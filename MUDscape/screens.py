import os
# TODO: Specify screen width and height


#depricated, use welcomMessage() instead
welcome_message = '''\
{YELLOW}       - Welcome to MUDScape -{RESET}\n


{RED}  ){RESET}       1.Enter Login             {RED})
{RED} ) \\{RESET}      2.Type "New"             {RED}) \\
{RED}/ {YELLOW}) {RED}(                             {RED}/ {YELLOW}) {RED}(
{RED}\{YELLOW}(_){RED}/                             {RED}\{YELLOW}(_){RED}/{RESET}
{WHITE}(|||)     World: 1                (|||)\
 |||        NULL Players           |||
 |||                               |||
 |||                               |||
(|||)    {BLUE}Copyright Jagex 1999{RESET}     (|||)'''

def welcomeMessage(players=0):
    message = '{YELLOW}' + '{:^39}'.format('- Welcome to MUDScape -') + '{RESET}' + os.linesep
    message +=  os.linesep + os.linesep
    message += '{RED}  ){RESET}' + '{:^33}'.format('1. Enter Login') + '{RED})' + os.linesep
    message += '{RED} ) \\{RESET}' + '{:^31}'.format('2. Type "New"') + '{RED}) \\' + os.linesep
    message += '{RED}\{YELLOW}(_){RED}/' + '{:^29}'.format('') + '{RED}\{YELLOW}(_){RED}/{RESET}' + os.linesep
    message +=  '{WHITE}(|||)' + '{:^29}'.format('World 1') + '(|||)' + os.linesep
    message += ' |||' + '{:^31}'.format(str(players) + ' Players') + '|||' + os.linesep
    message += ' |||' + '{:^31}'.format('') + '|||' + os.linesep
    message += ' |||' + '{:^31}'.format('') + '|||' + os.linesep
    message += '(|||){BLUE}' +  '{:^29}'.format('Copyright Jagex 1999') + '{WHITE}(|||)' + os.linesep
    return message