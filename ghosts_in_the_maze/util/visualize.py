import matplotlib.pyplot as plt
import openpyxl
import os 
import pandas as pd 






simulations = []
success = []
ghosts = []

#file = "AGENT-1.xlsx"
#data = pd.ExcelFile(file)
#print(data.sheet_names)


def visualize(file):
    os.chdir(os.getcwd())
    ps = openpyxl.load_workbook(file)
    
    sheet = ps[file]


    for row in range(2, sheet.max_row + 1):
        ghosts.append(sheet["A" + str(row)].value)
        success.append(sheet["B" + str(row)].value)
        simulations.append(sheet["C" + str(row)].value)

    plt.plot(success, ghosts)
    plt.title('Success Rate Vs Ghosts')
    plt.xlabel('Success Rate')
    plt.ylabel('Ghosts')
    plt.show()


visualize("AGENT-1.xlsx")



    




