
# import all functions from the tkinter 
from tkinter import *
# importing required libraries 
import requests, json, os 

# Create a GUI window 
root = Tk() 
root.title("Constraint writer GUI") 

	
# Function for clearing the Entry field 
def generate_const_json(): 
    constraints ={}
    constraints["critical_nets"] = []
    for net in CritNet_field.get().strip().split():
        crit ={"net":net,"value":def_criticality.get()}
        constraints["critical_nets"].append(crit)
    for net in CritNet_field1.get().strip().split():
        crit ={"net":net,"value":def_criticality1.get()}
        constraints["critical_nets"].append(crit)
    for net in CritNet_field2.get().strip().split():
        crit ={"net":net,"value":def_criticality2.get()}
        constraints["critical_nets"].append(crit)

    constraints["shielded_nets"] = []
    for net in ShieldNet_field.get().strip().split():
        snet ={"net":net,"value":s_net.get()}
        constraints["critical_nets"].append(snet)
    for net in ShieldNet_field1.get().strip().split():
        snet ={"net":net,"value":s_net1.get()}
        constraints["critical_nets"].append(snet)

    constraints["matching_blocks"]  =[]
    for blocks in MatchBlock_field.get().strip().split(';'):
        if blocks.strip():
            [block1,block2] = blocks.strip().split()
            match= {"block1":block1, "block2":block2}
            constraints["matching_blocks"].append(match)
    constraints["Symmetrical_nets"] = []
    for nets in SymmNet_field.get().strip().split(';'):
        if nets.strip():
            [net1, net2] = nets.strip().split(',')
            net1=net1.strip().split()
            net2=net2.strip().split()
            match= {"net1":net1[0], "net2":net2[0], "pins1":net1[1:-1] , "pins2":net2[1:-1]}
            constraints["Symmetrical_nets"].append(match)
    
    with open('constraint.json', 'w') as outfile:
        json.dump(constraints, outfile,indent =4)
def read_const_text():
    file_name = input_file.get().strip()
    constraints={}
    constraints["critical_nets"]=[]
    constraints["Symmetrical_nets"] = []
    constraints["shielded_nets"] = []
    constraints["matching_blocks"]  =[]
    constraints[""]  =[]
    if os.path.exists(file_name):
        with open(file_name) as fp:
            for line in fp:
                line= line.strip().replace(')','')
                if line:
                    if line.startswith("CritNet"):
                        [net,value] = line.strip().split('(')[1].split(',')
                        crit_const = {"net":net,"value":value}
                        constraints["critical_nets"].append(crit_const)
                    elif line.startswith("ShieldNet"):
                        net = line.strip().split('(')[1].replace(')','')
                        shield_const = {"net":net}
                        constraints["shielded_nets"].append(shield_const)
                    elif line.startswith("SymmNet"):
                        line = line.strip().split('(')[1]
                        [net1,net2] = line.split('}')[0:2]
                        #replace('},{','|').replace('{','').replace('}','').split('|')
                        net1=net1.strip().replace('{','').split(',')
                        net2=net2.strip().replace('{','').split(',')[1:-1]
                        match= {"net1":net1[0], "net2":net2[0], "pins1":net1[1:-1] , "pins2":net2[1:-1]}
                        constraints["Symmetrical_nets"].append(match)
                    elif line.startswith("MatchBlock"):
                        [block1,block2] = line.strip().split('(')[1].split(',')
                        match= {"block1":block1, "block2":block2}
                        constraints["matching_blocks"].append(match)
                    elif line.startswith("max_current"):
                        [net,value] = line.strip().split('(')[1].split(',')
                        current_const = {"net":net,"value":value}
                        constraints["max_current"].append(current_const)
                    else:
                        print("wrong input:%s",line)
    crit_net_min =[]
    crit_net_mid =[]
    crit_net_max =[]
    for nets in constraints["critical_nets"]:
        if 'min' in nets["value"]:
            crit_net_min.append(nets["net"])
        elif 'mid' in nets["value"]:
            crit_net_mid.append(nets["net"])
        elif 'max' in nets["value"]:
            crit_net_max.append(nets["net"])
    CritNet_field.insert(0,str(' '.join(crit_net_min)))
    CritNet_field1.insert(0,str(' '.join(crit_net_mid)))
    CritNet_field2.insert(0,str(' '.join(crit_net_max)))
    shield_net =[]
    for nets in constraints["shielded_nets"]:
        shield_net.append(nets["net"])
    symm_net =[]
    for match in constraints["Symmetrical_nets"]:
        symm_net.append(match["net1"]+' '+' '.join(match["pins1"])+','+match["net2"]+' '+' '.join(match["pins1"])+';')
    match_block =[]
    for match in constraints["matching_blocks"]:
        match_block.append(match["block1"]+' '+match["block2"]+';')

    ShieldNet_field.insert(0,str(' '.join(shield_net)))
    SymmNet_field.insert(0,str(' '.join(symm_net)))
    MatchBlock_field.insert(0,str(' '.join(match_block)))

# Driver code 
if __name__ == "__main__" : 
    """ 
    example inputs:
    Critical Nets: n1 n2
    Shield Nets: n1 n2 n3
    Match blocks: b1 b2; b3 b4
    Symmetrical nets: n1 p1 p2, n2 p22 p21; n2 p1,n3 p3
    """
    menu = Menu(root) 
    root.config(menu=menu) 
    filemenu = Menu(menu) 
    menu.add_cascade(label='File', menu=filemenu) 
    filemenu.add_command(label='New') 
    filemenu.add_command(label='Open...') 
    filemenu.add_separator() 
    filemenu.add_command(label='Exit', command=root.quit) 
    helpmenu = Menu(menu) 
    menu.add_cascade(label='Help', menu=helpmenu) 
    helpmenu.add_command(label='About')

    # Set the background colour of GUI window 
    root.configure(background = 'white') 
    
    # Set the configuration of GUI window (WidthxHeight) 
    root.geometry("600x400") 
    
    # Create welcome to Real Time Currency Convertor label 
    headlabel = Label(root, text = ' Welcome to constraint writer package', 
    				fg = 'black', bg = "cyan", pady=10) 
    
    label1 = Label(root, text = "Critical Nets :", fg = 'black', bg = 'slategray') 
    label2 = Label(root, text = "Shielded Nets(GND) :", fg = 'black', bg = 'slategray') 
    label3 = Label(root, text = "Match Blocks \n(; seperated pairs):", fg = 'black', bg = 'slategray') 
    label4 = Label(root, text = "Symmetrical Nets(pin list) :", fg = 'black', bg = 'slategray') 
    
    # grid method is used for placing the widgets at respective positions in table like structure . 
    headlabel.grid(row = 0, column = 1, sticky =W) 
    label1.grid(row = 1, column = 0 , columnspan=3, sticky =W, ipady=10) 
    label2.grid(row = 4, column = 0, columnspan=2, sticky =W, ipady=10) 
    label3.grid(row = 6, column = 0, sticky =W,ipady=4) 
    label4.grid(row = 8, column = 0, sticky =W,ipady =4) 
    #label5.grid(row = 10, column = 0) 
    
    # Create a text entry box 
    # for filling or typing the information. 
    CritNet_field = Entry(root) 
    CritNet_field1 = Entry(root) 
    CritNet_field2 = Entry(root) 
    CritNet_field.insert(0,"net1 net2") 
    ShieldNet_field = Entry(root)
    ShieldNet_field1 = Entry(root)
    ShieldNet_field.insert(0,"net1 net2") 
    MatchBlock_field = Entry(root)
    MatchBlock_field.insert(0,"block1 block2; block3 block4") 
    SymmNet_field = Entry(root)
    SymmNet_field.insert(0,"net1 pin1 pin2, net2 pina pinb; net3 pin1 pin2,net4 pina pinb") 
    input_file = Entry(root)
    input_file.insert(0,"<filename>") 
    
    # ipadx keyword argument set width of entry space. 
    CritNet_field.grid(row = 1, column = 1, ipadx ="40",ipady=5, sticky=N) 
    CritNet_field1.grid(row = 2, column = 1, ipadx ="40",ipady=5, sticky=N) 
    CritNet_field2.grid(row = 3, column = 1, ipadx ="40",ipady=5, sticky=N) 
    ShieldNet_field.grid(row = 4, column = 1, ipadx ="40",ipady=5) 
    ShieldNet_field1.grid(row = 5, column = 1, ipadx ="40",ipady=5) 
    MatchBlock_field.grid(row = 6, column = 1, ipadx ="40",ipady=5) 
    SymmNet_field.grid(row = 8, column = 1, ipadx ="40",ipady=5) 
    input_file.grid(row = 10, column = 1, ipadx ="40",ipady=5) 
    def_criticality = StringVar(root)
    def_criticality.set("min")
    def_criticality1 = StringVar(root)
    def_criticality1.set("mid")
    def_criticality2 = StringVar(root)
    def_criticality2.set("max")
    criticality = ["min","mid","max"] 
    criticality_option = OptionMenu(root, def_criticality, *criticality) 
    criticality_option.grid(row=1,column=2,ipadx=10)
    criticality_option1 = OptionMenu(root, def_criticality1, *criticality) 
    criticality_option1.grid(row=2,column=2,ipadx=10)
    criticality_option2 = OptionMenu(root, def_criticality2, *criticality) 
    criticality_option2.grid(row=3,column=2,ipadx=10)
    s_net = StringVar(root)
    s_net.set("GND")
    s_net1 = StringVar(root)
    s_net1.set("VDD")
    shield_nets = ["VDD","GND"] 
    criticality_option = OptionMenu(root, s_net, *shield_nets) 
    criticality_option.grid(row=4,column=2,ipadx=10)
    criticality_option1 = OptionMenu(root, s_net1, *shield_nets) 
    criticality_option1.grid(row=5,column=2,ipadx=10)
    
    # list of currency codes 
    #shild_options = ["VDD","VSS"] 
    
    # create a drop down menu using OptionMenu function 
    # which takes window name, variable and choices as 
    # an argument. use * befor the name of the list, 
    # to unpack the values 
    #shield_option = OptionMenu(root, shield_type, *) 
    #ToCurrency_option = OptionMenu(root, variable2, *CurrenyCode_list) 
    
    #FromCurrency_option.grid(row = 2, column = 1, ipadx = 10) 
    #ToCurrency_option.grid(row = 3, column = 1, ipadx = 10) 
    
    # Create a Convert Button and attached 
    # with RealTimeCurrencyExchangeRate function 
    #button1 = Button(root, text = "Convert", bg = "red", fg = "black", 
    #							command = RealTimeCurrencyConversion) 
    #
    #button1.grid(row = 4, column = 1) 
    
    # Create a Clear Button and attached 
    # with delete function 
    button1 = Button(root, text = "Read constraint from text file", bg = "cyan", 
    				fg = "black", command = read_const_text) 
    button1.grid(row = 10, column = 0) 
    button2 = Button(root, text = "Generate constraint json", bg = "green", 
    				fg = "black", command = generate_const_json) 
    button2.grid(row = 12, column = 1) 
    
    # Start the GUI 
    root.mainloop() 
