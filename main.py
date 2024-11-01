import pandas as pd
import tkinter
import variables
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

PATHOGENS_FILENAME = "csv_sources/pathogenic_associations.csv"
ZOO_BACTERIA_FILENAME = "csv_sources/zoonotic-bacteria.csv"
ZOO_VIRUS_FILENAME = "csv_sources/zoonotic-virus.csv"

RESULT_PAT_FILENAME = "result_pathogens.xlsx"
RESULT_BAC_FILENAME = "result_bacteria.xlsx"
RESULT_VIR_FILENAME = "result_viruses.xlsx"


def main():

    main_window = tkinter.Tk()
    main_window.geometry("400x250+200+200")
    main_window.title('METAGEN')
    main_window.iconbitmap("icon_dna.ico")


    metadata_filename = variables.InputVariable().get_metadata()

    metadata_frame = tkinter.Frame(main_window)
    metadata_placeholder = tkinter.StringVar(value=metadata_filename)
    metadata_label = tkinter.Label(metadata_frame,text='Metadata file', borderwidth=1, relief='flat')
    metadata_label.pack(side='left',padx=(20,22), pady=15, ipadx=5, ipady=5)
    metadata_entry = tkinter.Entry(metadata_frame, textvariable=metadata_placeholder, width=21) 
    metadata_entry.pack(side='right', padx=(20,50))
    metadata_frame.pack(anchor='nw')


    fragments_filter = variables.InputVariable().get_filter()
    search_db = variables.InputVariable().get_search_db()
    
    #filter frame
    filter_frame = tkinter.Frame(main_window)   
    filter_label = tkinter.Label(filter_frame,text='Fragments filter',borderwidth=1, relief='flat')
    filter_label.pack(side='left',padx=(20,5), pady=15, ipadx=5, ipady=5)

    filter_placeholder = tkinter.StringVar(value=fragments_filter)
    filter_entry = tkinter.Entry(filter_frame, textvariable=filter_placeholder, width=21)
    filter_entry.pack(side='right', padx=(22,50))
    filter_frame.pack(anchor='nw')

    #search db frame
    db_frame = tkinter.Frame(main_window)   
        
    db_list = ['Human Pathogens', 'Bacteria', 'Viruses']
    db_placeholder = tkinter.StringVar(value=search_db)
    
    db_combobox = ttk.Combobox(db_frame,values= db_list, textvariable=db_placeholder, width=18, state='readonly')
    db_label = tkinter.Label(db_frame,text='Select db to search',borderwidth=1, relief='flat')
        
        
    db_label.pack(side='left',padx=(20,5), pady=15, ipadx=5, ipady=5)
    db_combobox.pack(side='right', padx=6, pady=6)
        
    db_frame.pack(anchor='nw')


    go_button(main_window, metadata_entry,filter_entry,db_combobox)
    
 
    tkinter.mainloop()  



    
def go_button(main_window, metadata_entry,filter_entry,db_combobox):   
    go_frame = tkinter.Frame(main_window)
    go_button = ttk.Button(go_frame, text='Go', command=lambda:go_command(metadata_entry,filter_entry,db_combobox))
    go_button.pack(side='right',padx=(20,5), pady=15)
    go_frame.pack()

def go_command(metadata_entry,filter_entry,db_combobox):

    metadata_filename = metadata_entry.get()
    fragments_filter = int(filter_entry.get())
    search_db = db_combobox.get()

    metadata_row = pd.read_csv(metadata_filename)
    metadata = metadata_row[(metadata_row["Number of fragments root"] > fragments_filter) & (metadata_row["Rank code"] == "S")] #TODO добавить использование кол-ва фрагментов

    for column in metadata.columns:
        if metadata[column].dtype == object:
            metadata[column] = metadata[column].map(str.strip)

    if search_db == "Human Pathogens":

        pathogens = pd.read_csv(PATHOGENS_FILENAME)
        result_pathogens = pd.merge(metadata, pathogens, on="TaxID").sort_values(by="Number of fragments root", ascending=False)
        result_pathogens = result_pathogens.assign(Taxon=result_pathogens["Name"])
        result_pathogens = result_pathogens[["% Classified", "Number of fragments root", "TaxID","Taxon", "Pathogenic associations" ]]
        #result_pathogens.to_csv(RESULT_PAT_FILENAME)
        result_pathogens.to_excel(RESULT_PAT_FILENAME)

        res = result_pathogens


    elif search_db == "Bacteria":    
        zoo_bacteria = pd.read_csv(ZOO_BACTERIA_FILENAME)
        result_bacteria = pd.merge(metadata, zoo_bacteria, on="Taxon")[["% Classified", "Number of fragments root", "Taxon", "Zoonotic"]].sort_values(by="Number of fragments root", ascending=False)
        #result_bacteria.to_csv(RESULT_BAC_FILENAME)
        result_bacteria.to_excel(RESULT_BAC_FILENAME)
        res = result_bacteria
    


    elif search_db == "Viruses":   
        zoo_viruses = pd.read_csv(ZOO_VIRUS_FILENAME)
        result_viruses = pd.merge(metadata, zoo_viruses, on="Taxon")[["% Classified", "Number of fragments root", "Taxon", "Zoonotic", "GenomeType"]].sort_values(by="Number of fragments root", ascending=False)
        #result_viruses.to_csv(RESULT_VIR_FILENAME)
        result_viruses.to_excel(RESULT_VIR_FILENAME)
        res = result_viruses

    else: 
        print("select one option")
    
    show_result(res)



def show_result(res):
    limit = "10"
    x_coord = range (1,11)

    result_figure = res[[ "Number of fragments root","Taxon"]].head(10)

    names = result_figure["Taxon"].to_list()

    heights = result_figure["Number of fragments root"].to_list()

    max = len(heights)

    if max < 11:
        x_coord = range(1,(max+1))
    else:
        x_coord = range(1,(int(limit)+1))

    
    figure_window = tkinter.Tk()
    figure_window.title(f"Top Results ")
    fig = Figure(figsize=(9, 5), dpi=100)
    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom=0.25,left=0.2) #это отступы от краев


    ax.bar(x_coord, heights, color='k')
    ax.set_ylabel('Number of fragments')
    ax.set_xticks(x_coord)
    ax.set_xticklabels(names,rotation=30, ha = 'right')
 
    ax.set_autoscaley_on
    fig.savefig("result_figure.png")
    
    canvas = FigureCanvasTkAgg(fig, master=figure_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    figure_window.mainloop()


if __name__ == '__main__':
    main() 
