# MedieScolastiche
GUI program for the average of school grades written in python using PyQt5 for GUI and MatPlotLib for charts

## Getting Started
To use this program, read the following instructions

>These instructions are based on GNU/Linux systems. If you want to help me open an docs issue and instructions based on your platform

### Download the program
First of all, check if "git" is installed on your machine. The output should look like this
```
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]
```
If the output is like this
```
Command 'git' not found
```
you have to install git typing
```
sudo apt install git
```

After that, type
```
git clone https://github.com/seepiol/MedieScolastiche.git
```

go into the directory using 
```
cd MedieScolastiche
```

and install the requirements using
```
python3 -m pip install -r ./requirements.txt
```

### Run the program
In the MedieScolastiche folder, run the program with
```
python3 main.py
```

## Using the program

![mainvindow](https://user-images.githubusercontent.com/60071372/73024965-02d32b00-3e2f-11ea-9193-908618a3c848.png)

From this Window you can insert the subject name, the test score and the date of the test. 
By clicking "Add" the test will be saved. You can create multiple subjects changing the name. At the end of the insertion, click "Media" button.

The window that will appear will be like this

![averagewindow](https://user-images.githubusercontent.com/60071372/73024979-08307580-3e2f-11ea-9b87-e2a249f2ea86.png)

If you click "Grafico Materia", will be created the graph for the selected subject.

![subjectgraph](https://user-images.githubusercontent.com/60071372/73025072-3910aa80-3e2f-11ea-9cb7-fb7a3ba322ff.png)

If you click on "Grafico Situazione" instead, the graph is the one about the general situation. 

![situationgraph](https://user-images.githubusercontent.com/60071372/73025077-3ada6e00-3e2f-11ea-96cc-0337787fd0eb.png)

# Save the data
You can save your tests data in a csv file, compatible with all spreadsheets programs (We suggest **[LibreOffice](https://www.libreoffice.org/) Calc** )

> **Under Development**