import subprocess
from subprocess import check_output

p = subprocess.Popen([r'C:\Users\Rex\PycharmProjects\pythonProject\win.bat'], stdout=subprocess.PIPE)
out, err = p.communicate()

#result=subprocess.call([r'C:\Users\Rex\PycharmProjects\pythonProject\win.bat'])


proc = subprocess.Popen("bat "+'C:\\Users\\Rex\\PycharmProjects\\pythonProject\\win.bat', shell=True,
                        stdout=subprocess.PIPE)
script_response = proc.stdout.read()
run_result_php = script_response.decode('UTF-8')


#print(out)






