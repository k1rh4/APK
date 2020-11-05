# -*- coding: utf-8 -*-
from com.pnfsoftware.jeb.util.encoding.IntegerLEB128 import DecodedInt
from com.pnfsoftware.jeb.core.units.code.asm.processor import AbstractProcessor

from com.pnfsoftware.jeb.core.util import DecompilerHelper 
from com.pnfsoftware.jeb.client.api import IScript, IconType, ButtonGroupType 
from com.pnfsoftware.jeb.core import RuntimeProjectUtil 
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem 
from com.pnfsoftware.jeb.core.output.text import TextDocumentUtil
from com.pnfsoftware.jeb.core.units import INativeCodeUnit
from java.lang import Runnable

from com.pnfsoftware.jeb.core.actions import Actions, ActionContext, ActionXrefsData
from com.pnfsoftware.jeb.core.actions import ActionRenameData 

LOGLIST=["Log;->i", "Log;->d", "Log;->e", "Log;->w"]

class renameClass(IScript):
  def run(self, ctx):
    # For non-ASCII characters, remember to specify the encoding in the script header (here, UTF-8),
    # and do not forget to prefix all Unicode strings with "u", whether they're encoded (using \u or else) or not
    print("Let's Start ")
    ctx.executeAsync("Decompiling all...", Decomp(ctx))
    print ("END...")

class Decomp(Runnable):
  def __init__(self, ctx):
    self.ctx = ctx 

  def run(self):
    self.outputDir = self.ctx.getBaseDirectory()
    prj = self.ctx.getMainProject() 
  
    for codeUnit in prj.findUnits(ICodeUnit):
      #print("->:%s %s" %(str(codeUnit.getName()), type(codeUnit.getName())))
      if( str(codeUnit.getName()) != "Bytecode"):
        continue 

      for class_ctx in codeUnit.getClasses() :
        for method_ctx in class_ctx.getMethods(): 
          ### DEBUGGING ###
          #if( not "Aa" in str(class_ctx) ):
          if( not "Aa" in str(class_ctx) or "hide" != method_ctx.getName() ):
              #continue
              pass

          ### RELEASE ### 
          #print("[D] interator class name: "+str(class_ctx.getName()))
          if(len(class_ctx.getName()) > 2 or ("$" in str(method_ctx))) :
            continue 

          logTagName = self.isInvokeStatic(codeUnit, method_ctx)
          className = method_ctx.getClassType().getAddress()
          logTagName = logTagName.replace("-","_").replace(".","_")
          if( "none" in logTagName or "$" in logTagName): 
            continue
          else:
            self.commenceRename(codeUnit, className, logTagName )


  def isInvokeStatic(self, codeUnit, methodUnit):
    params = [ "none" for _ in range(0,100) ]
    #print("[D] getClass->" + str(methodUnit.getClassType().getAddress()))
    if( not methodUnit.getInstructions() ) :
      #print ("[D] not interatable")
      return "none"

    for inst in methodUnit.getInstructions():
      if( inst.getMnemonic() in ("const-string") ):
        index   = int(inst.getParameters()[0].getValue())
        string  = codeUnit.getString(inst.getParameters()[1].getValue()) 
        params[index] = string 

      elif(inst.getMnemonic() in ("invoke-static")):
        func_num = codeUnit.getMethod(inst.getParameters()[0].getValue()) 
        #print(func_num)
        for LOG in LOGLIST : 
          if( LOG in str(func_num.getAddress()) ):
            #print(inst.getParameters())
            #print(inst.getParameters()[1].getValue())
            index= int(inst.getParameters()[1].getValue())
            
            #print("[D] %s ::: ( %s )" %(func_num.getAddress(), params[index]))
            if( not "none" in str(params[0])):
              return str(params[index])
      else:
        pass
    return "none"
   

  def commenceRename(self, codeUnit, ClassName, newName):
    clz = codeUnit.getClass(ClassName)
    #clz = codeUnit.getMethod(ClassName)
    print("[+] Change class name from [ %s ] to [ %s ] " %( ClassName, newName ) )
    #print(clz)

    actCntx = ActionContext(codeUnit, Actions.RENAME, clz.getItemId(), clz.getAddress())
    actData = ActionRenameData()
    actData.setNewName(newName)

    if(codeUnit.prepareExecution(actCntx, actData)):  
        try:
          bRlt = codeUnit.executeAction(actCntx, actData)  
          if(not bRlt):  
            print(u'executeAction fail!')  
        except Exception,e:  
          print Exception,":",e