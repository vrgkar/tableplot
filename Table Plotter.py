import mysql.connector as sqltor
import matplotlib.pyplot as plt
import os
import pickle
import csv

def closestFactors(n):
    sqn = int(n**0.5)
    
    while n % sqn != 0:
        sqn -= 1
    
    return (sqn, n // sqn)
        
class Plot:
    
    def __init__(self):
        self.m_graphs = []
        
    def append(self, graph):
        self.m_graphs.append(graph)
        
    def plot(self):
        if not self.m_graphs:
            print("\nNo Graphs to Plot!\n")
            return
            
        rows, columns = closestFactors(len(self.m_graphs))
        
        for i in range(len(self.m_graphs)):
            plt.subplot(rows, columns, i+1)
            self.m_graphs[i].plot()
            
        plt.show()
        
    def remove(self):
        print("-----Graph Deletion Menu------")
        
        for i in range(len(self.m_graphs)):
            print(f"{i+1}.", self.m_graphs[i].title())
            
    m_graphs = None
    

class Graph:
    
    def __init__(self):
        self.m_db = ''
        self.m_tb = ''
        self.m_table = []
        
    def title(self):
        return self.m_title
    
    def load(self, curs):
        curs.execute("SHOW databases;")
        
        databases = curs.fetchall()
        
        while True:
            print("\n-------Select a Database-------")
            for i in range(len(databases)):
                print(f"{i+1}.", databases[i][0])
    
            db_choice = int(input())
    
            if db_choice <= len(databases) and db_choice > 0:
                self.m_db = databases[db_choice-1][0]
                break
    
            print("\nDatabase selected is not in the list of available databases. Please try again.\n")
        
        curs.execute(f"USE {self.m_db};")
        curs.execute("SHOW tables;")

        tables = curs.fetchall()
        
        while True:
            print("\n-------Select a Table-------")

            for i in range(len(tables)):
                print(f"{i+1}.", tables[i][0])
    
            tb_choice = int(input())
    
            if tb_choice <= len(tables) and tb_choice > 0:
                self.m_tb = tables[tb_choice-1][0]
                break
    
            print("\nTable selected is not in the list of available tables. Please try again.\n")
            
        curs.execute(f"DESC {self.m_db}.{self.m_tb};")
        self.m_table.append(tuple([i[0] for i in curs]))
        
        curs.execute(f"SELECT * FROM {self.m_db}.{self.m_tb};")
        self.m_table.extend(curs.fetchall())
        
        self.m_title = input("\nEnter Title of Graph: ")
        
    def save(self):
        with open('data.csv', 'a') as f:
            writer = csv.writer(f)

            writer.writerow([self.m_title, self.m_table])

    def plot(self):
        pass
              
    m_db = None
    m_tb = None
    m_title = None
    m_table = None
    
    
class LineGraph(Graph):
    
    def __init__(self):
        super().__init__()
        self.m_xvalues, self.m_yvalues = [], []
        
    def plot(self):  
        plt.plot(self.m_xvalues, self.m_yvalues)
        plt.xlabel(self.m_xlabel)
        plt.ylabel(self.m_ylabel)
        plt.title(self.m_title)
        
        
    def load(self, curs):
        super().load(curs)
        
        while True:
            print("--------Graph Creation Menu--------")
            
            menu_choice = int(input("1. Set Graph Values\n2. Preview Graph\n3. Save and Exit and Append to Plot\nChoose an option: "))
        
            if menu_choice == 1:
                
                while True:
                    
                    for i in self.m_table:
                        print(i)
                        
                    create_choice = int(input("\n1. X Values\n2. Y Values\n3. Done\nChoose an option: "))
                    
                    if create_choice == 1:
                        
                        self.m_xvalues = []
                        
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input("\nChoose a column: "))
                        
                        for i in self.m_table[1:]:
                            self.m_xvalues.append(i[column_choice-1])
                            
                        self.m_xlabel = self.m_table[0][column_choice-1]
                    
                    elif create_choice == 2:
                        
                        self.m_yvalues = []
                        
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input("\nChoose a column: "))
                        
                        for i in self.m_table[1:]:
                            self.m_yvalues.append(i[column_choice-1])
                            
                        self.m_ylabel = self.m_table[0][column_choice-1]
                        
                    elif create_choice == 3:
                        break
            
            elif menu_choice == 2:
                
                plt.plot(self.m_xvalues, self.m_yvalues)
                plt.xlabel(self.m_xlabel)
                plt.ylabel(self.m_ylabel)
                plt.title(self.m_title)
                    
                plt.show()
            
            elif menu_choice == 3:
                self.save()
                break

    m_xvalues, m_xlabel = None, None
    m_yvalues, m_ylabel = None, None
     

class PieGraph(Graph):
    
    def __init__(self):
        super().__init__()
        self.m_values = []
        self.m_labels = []
        self.m_title = self.m_tb
    
    def plot(self):
        plt.pie(self.m_values, labels=self.m_labels)
        plt.title(self.m_title)
            
    
    def load(self, curs):
        super().load(curs)
        
        while True:
            print("--------Graph Creation Menu--------")
            
            menu_choice = int(input("1. Set Graph Values\n2. Preview Graph\n3. Save and Exit and Append to Plot\n"))
        
            if menu_choice == 1:
                    
                while True:
                    
                    for i in self.m_table:
                        print(i)
                        
                    create_choice = int(input("\n1. Values\n2. Labels\n3. Done\n"))
                    
                    if create_choice == 1:
                        
                        self.m_values = []
                        
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input("\nChoose a column: "))
                        
                        for i in self.m_table[1:]:
                            self.m_values.append(i[column_choice-1])
                    
                    elif create_choice == 2:
                        
                        self.m_labels = []
                        
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input("\nChoose a column: "))
                        
                        for i in self.m_table[1:]:
                            self.m_labels.append(i[column_choice-1])
                                      
                    elif create_choice == 3:
                        break
            
            elif menu_choice == 2:
                
                plt.pie(self.m_values, labels=self.m_labels)
                plt.title(self.m_title)
                    
                plt.show()
            
            elif menu_choice == 3:
                self.save()
                break
        
        
    m_values = None
    m_labels = None
    

class ScatterGraph(Graph):
    
    def __init__(self):
        super().__init__()
        self.m_xvalues, self.m_yvalues = [], []
        
    def plot(self):  
        plt.scatter(self.m_xvalues, self.m_yvalues)
        plt.xlabel(self.m_xlabel)
        plt.ylabel(self.m_ylabel)
        plt.title(self.m_title)
        
        
    def load(self, curs):
        super().load(curs)
        
        while True:
            print("--------Graph Creation Menu--------")
            
            menu_choice = int(input("1. Set Graph Values\n2. Preview Graph\n3. Save and Exit and Append to Plot\nChoose an option: "))
        
            if menu_choice == 1:
                
                while True:
                    
                    for i in self.m_table:
                        print(i)
                        
                    create_choice = int(input("\n1. X Values\n2. Y Values\n3. Done\nChoose an option: "))
                    
                    if create_choice == 1:
                        
                        self.m_xvalues = []
                        
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input("\nChoose a column: "))
                        
                        for i in self.m_table[1:]:
                            self.m_xvalues.append(i[column_choice-1])
                            
                        self.m_xlabel = self.m_table[0][column_choice-1]
                    
                    elif create_choice == 2:
                        
                        self.m_yvalues = []
                        
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input("\nChoose a column: "))
                        
                        for i in self.m_table[1:]:
                            self.m_yvalues.append(i[column_choice-1])
                            
                        self.m_ylabel = self.m_table[0][column_choice-1]
                        
                    elif create_choice == 3:
                        break
            
            elif menu_choice == 2:
                
                plt.scatter(self.m_xvalues, self.m_yvalues)
                plt.xlabel(self.m_xlabel)
                plt.ylabel(self.m_ylabel)
                plt.title(self.m_title)
                    
                plt.show()
            
            elif menu_choice == 3:
                self.save()
                break

    m_xvalues, m_xlabel = None, None
    m_yvalues, m_ylabel = None, None


class BarGraph(Graph):
    
    def __init__(self):
        super().__init__()
        self.m_values = []
        self.m_labels = []
        self.m_title = self.m_tb
    
    def plot(self):
        plt.bar(self.m_labels, self.m_values)
        plt.title(self.m_title)
            
    
    def load(self, curs):
        super().load(curs)
        
        while True:
            print("--------Graph Creation Menu--------")
            menu_choice = int(input("1. Set Graph Values\n2. Preview Graph\n3. Exit and Append to Plot\nChoose an option: "))
        
            if menu_choice == 1:
                    
                while True:
                    
                    for i in self.m_table:
                        print(i)
                        
                    create_choice = int(input("\n1. Values\n2. Labels\n3. Done\n"))
                    
                    if create_choice == 1:
                        
                        self.m_values = []
                        
                        print("Choose a column for Values:")
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input())
                        
                        for i in self.m_table[1:]:
                            self.m_values.append(i[column_choice-1])
                    
                    elif create_choice == 2:
                        
                        self.m_labels = []
                        
                        print("Choose a column for Labels:")
                        for i in range(len(self.m_table[0])):
                            print(f"{i+1}.", self.m_table[0][i])
                            
                        column_choice = int(input())
                        
                        for i in self.m_table[1:]:
                            self.m_labels.append(i[column_choice-1])
                                      
                    elif create_choice == 3:
                        break
            
            elif menu_choice == 2:
                
                plt.bar(self.m_labels, self.m_values)
                plt.title(self.m_title)
                    
                plt.show()
            
            elif menu_choice == 3:
                self.save()
                break
        
        
    m_values = None
    m_labels = None
        

class Application:
    
    def __init__(self):
        
        print("-------MySQL Login--------")
        sqluser = input("Username: ")
        sqlpasswd = input("Password: ")

        self.m_con = sqltor.connect(host='localhost', user=sqluser, passwd=sqlpasswd)

        if not self.m_con.is_connected():
            return
        
        print("\nSuccessfully Connected to MySQL database\n")
        
        self.m_plot = Plot()
        self.m_curs = self.m_con.cursor()
        self.m_running = True

    def mainloop(self):
        
        while app.running():

            print("--------TABLE PLOTTER MENU--------")
            menu_choice = int(input("1. Create\n2. Delete\n3. Plot\n4. Save\n5. Load\n6. Exit\n"))
            
            if menu_choice == 1:

                print("--------Choose a graph type--------")
                graph_choice = int(input("\n1. Line Graph\n2. Bar Graph\n3. Pie Chart\n4. Scatter Graph\n5. Go back\n"))
                
                if graph_choice == 1:
                    graph = LineGraph()
                    graph.load(self.m_curs)
                    self.m_plot.append(graph)
                    
                elif graph_choice == 2:
                    graph = BarGraph()
                    graph.load(self.m_curs)
                    self.m_plot.append(graph)
                    
                elif graph_choice == 3:
                    graph = PieGraph()
                    graph.load(self.m_curs)
                    self.m_plot.append(graph)
                    
                elif graph_choice == 4:
                    graph = ScatterGraph()
                    graph.load(self.m_curs)
                    self.m_plot.append(graph)
                    
                elif graph_choice == 5:
                    pass
                
            elif menu_choice == 2:
                print("-----Graph Deletion Menu------")
                
                while True:
                    
                    for i in range(len(self.m_plot.m_graphs)):
                        print(f"{i+1}.", self.m_plot.m_graphs[i].title())

                    print(f"{len(self.m_plot.m_graphs)+1}.", "Exit")
                    
                    deletion_choice = int(input())
                
                    if deletion_choice <= len(self.m_plot.m_graphs) and deletion_choice >= 1:
                        del self.m_plot.m_graphs[deletion_choice-1]
                        
                    if deletion_choice == len(self.m_plot.m_graphs) + 1:
                        break  
            
            elif menu_choice == 3:
                self.m_plot.plot()

            elif menu_choice == 4:
                
                key = input("Enter a key for the current plot: ")
                plots = []
                
                if os.path.exists('saved_plots.dat'):
                    with open('saved_plots.dat', 'rb') as dat:
                        plots = pickle.load(dat)
                    
                with open('saved_plots.dat', 'wb') as dat:
                    plots.append([self.m_plot, key])
                    pickle.dump(plots, dat)

            elif menu_choice == 5:

                if not os.path.exists('saved_plots.dat'):
                    print("Saved plots file doesn't exist")
                    continue
                
                if self.m_plot.m_graphs:
                    print("WARNING! Will Destroy current plot!")
                    ans = input("Continue? [y/n]")

                    if ans.lower() != 'y':
                        continue
                
                key = input("\nEnter key of the plot: ")

                with open('saved_plots.dat', 'rb') as f:
                    dat = pickle.load(f)

                for i in dat:  
                    if key == i[1]:
                        self.m_plot = i[0]
                        break
                else:
                    print(f"Plot with key:{key} not found")
                    
                            
            elif menu_choice == 6:
                self.m_running = False
            
    def running(self):
        return self.m_running
            
    m_con = None
    m_curs = None
    m_plot = None
    m_running = False

app = Application()
app.mainloop()



        



    
