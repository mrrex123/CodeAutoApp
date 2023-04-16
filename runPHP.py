import subprocess
from subprocess import Popen, PIPE


#subprocess.call("php C:\\Users\\Rex\\PycharmProjects\\pythonProject\\phpTest.php")

# if you want output
#proc = subprocess.Popen("php C:\\Users\\Rex\\PycharmProjects\\pythonProject\\phpTest.php", shell=True,
 #                       stdout=subprocess.PIPE)
#script_response = proc.stdout.read()

#print(script_response)


def php(code):
    p = subprocess.Popen(["php", "-r", code],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate() #returns a tuple (stdoutdata, stderrdata)
    if out[1] != b'': raise Exception(out[1].decode('UTF-8'))
    return out[0].decode('UTF-8')
'''
code = """ \
  $a = ['a', 'b', 'c'][2]; \
  echo($a);"""
  
  '''
code = """  $a=22; $b=21; $c=$a + $b;
  echo("rex".$c);"""
#print(php(code))


jcode=''' 
        
      int num1 = 5, num2 = 15, sum;
      sum = num1 + num2;

      System.out.println("Sum of these numbers: "+sum);
   
 '''

'''
def java(jcode):
    p = subprocess.Popen(["javac", "-r", jcode],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()  # returns a tuple (stdoutdata, stderrdata)
    if out[1] != b'': raise Exception(out[1].decode('UTF-8'))
    return out[0].decode('UTF-8')

print(java(jcode))
 
import subprocess
ccmd = ['javac', 'T.java']
process = subprocess.Popen(ccmd)
process.wait()
rcmd = ['java', 'T']
output = ""
process = subprocess.Popen(rcmd, stdout=subprocess.PIPE)
output = process.stdout.read()
print output,

'''