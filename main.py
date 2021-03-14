from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import random
import numpy as np
from fractions import Fraction as fr

#from kivy.uix.button import Button
# eliminar text=str(random.randrange(1,10)) cuando este la app
class Gridd(GridLayout):
    pass
class HBoxTable(BoxLayout):
    pass
class VBoxTable(BoxLayout):
    pass
class LabelTable(MDLabel):
    pass

class MainUI(BoxLayout):
    dialog = None
    def click(self):
        self.variables = int(self.ids.txt_var.text) if self.ids.txt_var.text != '' else 0
        self.restricciones = int(self.ids.txt_res.text) if self.ids.txt_res.text != '' else 0
        #BoxLayout.height
        
        #se guardaran los input
        self.gTInputVar = {}
        scroll = self.ids.scroll
        #para crear las variables
        for i in range(0,self.variables):
            bInput = MDBoxLayout(size_hint_x=None,width= '30px')
            id = f'x{str(i+1)}'
            self.gTInputVar[i] = TextInput(size_hint_x=None,width='30px')
            bInput.add_widget(self.gTInputVar[i])
            if i+1!=self.variables:
                bLabel = MDBoxLayout(size_hint_x=None,width= '35px',padding= (2,0,0,0))
                bLabel.add_widget(MDLabel(text=f'X{str(i+1)} +',theme_text_color= "Custom",text_color= (1, 1, 1, 1)))
            else:
                bLabel = MDBoxLayout(size_hint_x=None,width= '25px',padding= (2,0,0,0))
                bLabel.add_widget(MDLabel(text=id,theme_text_color= "Custom",text_color= (1, 1, 1, 1)))
            scroll.add_widget(bInput)
            scroll.add_widget(bLabel)
        #para crear las restricciones
        #se guardaran los input
        self.gTInputRes = {}
        self.table0=[]
        # se aumentan 2 1 para la nueva columna y otra para la de valores finales
        newRes = self.variables+1
        for i in range(0,self.restricciones):
            height = self.restricciones*30
            Hbox = MDBoxLayout(orientation='horizontal',md_bg_color=(.7,.35,.5,1),size_hint_y=None,height='30px')
            ContainerNres = MDBoxLayout(size_hint_x=None,width='35px',md_bg_color= (.3,.5,.7,1),padding= (10,0,5,0))
            Nres = MDLabel(theme_text_color= "Custom",text_color= (1, 1, 1, 1),text=f'{i+1}',halign='center')
            ScrollV = ScrollView()
            Grid = Gridd()
            ContainerNres.add_widget(Nres)
            #para los valores de las columnas que van 0 en la tabla
            
            #para cada columna crear su input y su label 
            #las columnas va acorde a las variables
            for j in range(0,newRes):
                bInput = MDBoxLayout(size_hint_x=None,width= '30px')
                id = f'x{str(j+1 +i)}'               
                #para la ultima fila hay que eliminar ramdom y dejarlo vacio
                randomyultimo = str("") if (j+1!=newRes)else str(1)
                self.gTInputRes[f'f{i},c{j}'] = TextInput(size_hint_x=None,width='30px',text=randomyultimo)
                bInput.add_widget(self.gTInputRes[f'f{i},c{j}'])
                if j+1!=newRes:
                    bLabel = MDBoxLayout(size_hint_x=None,width= '35px',padding= (2,0,0,0))
                    bLabel.add_widget(MDLabel(text=f'X{str(j+1)} +',theme_text_color= "Custom",text_color= (1, 1, 1, 1)))
                    Grid.add_widget(bInput)
                    Grid.add_widget(bLabel)
                else:
                    self.table0.append(j+1+i)
                    bLabel = MDBoxLayout(size_hint_x=None,width= '30px',padding= (2,0,0,0))
                    bLabel.add_widget(MDLabel(text=id,theme_text_color= "Custom",text_color= (1, 1, 1, 1)))
                    bInputSig = MDBoxLayout(size_hint_x=None,width= '30px')
                    self.gTInputRes[f'f{i},c{j+1}'] = TextInput(size_hint_x=None,width='30px')
                    
                    bLabelSig = MDBoxLayout(size_hint_x=None,width= '25px',padding= (2,0,0,0))
                    bLabelSig.add_widget(MDLabel(text='<=',theme_text_color= "Custom",text_color= (1, 1, 1, 1)))
                    
                    Grid.add_widget(bInput)
                    Grid.add_widget(bLabel)
                    Grid.add_widget(bLabelSig)
                    bInputSig.add_widget(self.gTInputRes[f'f{i},c{j+1}'])
                    Grid.add_widget(bInputSig)
                    
                

            ScrollV.add_widget(Grid)
            Hbox.add_widget(ContainerNres)
            Hbox.add_widget(ScrollV)
            self.ids.contentRes.height = f'{height}px'
            self.ids.contentRes.add_widget(Hbox)
        
            


    def comenzar(self):
        self.ids.crear.disabled = True
        #mapa de cada fila o diccionario de datos
        self.fMap={}
        #global nuevo almacen de variables para la tabla generada
        self.ArrTable ={}
        #cantidad de restricciones
        NRes = self.restricciones
        #cantidad de variables
        NVar = self.variables
        #aumento de restricciones cantidad e de variables + las restricciones
        ARes = NRes + NVar
        #cantidad de filas ya agregando las 4 de nombres de celdas 
        f = NRes + 4
        # cantidad de columnas ya agregando las 3 de nombres de celdas
        c = ARes + 3
        # id de la tabla estoy trabajando fila a fila
        table = self.ids.table
        #filas
        aume = NVar
        # inputs de las variables 
        IVar = self.gTInputVar
        # inputs de las restricciones
        IRes = self.gTInputRes
        #por que no entra al proceso de utilizacion hasat
        iR=0
        parte0 = 0
        for i in range(0,f):
            cArr =[]
            #solo aumenta a partir de la fila 2 has laf-1
            if i>1 and i<f-1:
                aume += 1
            fTable = HBoxTable()
            #columnas
            primeraF = 0
            
            jR=0
            
            for j in range(0,c):
                cTable = VBoxTable()
                #para la parte de los 0
                
                #fila 0
                if i==0:
                    if j==0:
                        f0c0Label = LabelTable(text='')
                        cTable.add_widget(f0c0Label)
                    if j==1:
                        f0c1Label = LabelTable(text='Cj')
                        cTable.add_widget(f0c1Label)
                    if j>1 and j<c-1:
                        #para sacar los valores del input mediante un contador
                        if primeraF != NVar:
                            text = IVar[primeraF].text
                            #debo guardar el label para poder reut
                            self.ArrTable[f'f{i},c{j}'] = LabelTable(text=f'{text}')
                            cTable.add_widget(self.ArrTable[f'f{i},c{j}'])
                            cArr.append(self.ArrTable[f'f{i},c{j}'])
                            primeraF+=1
                        else:
                            self.ArrTable[f'f{i},c{j}'] = LabelTable(text='0')
                            cTable.add_widget(self.ArrTable[f'f{i},c{j}'])
                            cArr.append(self.ArrTable[f'f{i},c{j}'])
                #para la fila 1
                if i==1:
                    if j==0:
                        f1c0Label = LabelTable(text='Cb')
                        cTable.add_widget(f1c0Label)
                    if j==1:
                        f1c1Label = LabelTable(text='Xb')
                        cTable.add_widget(f1c1Label)
                    if j>1 and j<c-1:
                        f1c2Label = LabelTable(text=f'X{str(j-1)}')
                        cTable.add_widget(f1c2Label)
                    if j ==c-1:
                        f1cuLabel = LabelTable(text=f'Bi')
                        cTable.add_widget(f1cuLabel)
                if i>1 and i <f-2:
                    if j==0:
                        self.ArrTable[f'f{i},c{j}'] = LabelTable(text='0')

                        #self.CjMap[f'f{i}c{j}']=0

                        cTable.add_widget(self.ArrTable[f'f{i},c{j}'])
                        cArr.append(self.ArrTable[f'f{i},c{j}'])
                    if j ==1:
                        #esta estatico
                        f2c1Label = LabelTable(text=f'X{aume}')
                        cTable.add_widget(f2c1Label)
                    if j>1:
                        
                        if iR < self.restricciones and jR< self.variables :
                            #print(iR,jR)
                            v= IRes[f'f{iR},c{jR}'].text
                            self.ArrTable[f'f{i},c{j}'] = LabelTable(text=v)
                            cTable.add_widget(self.ArrTable[f'f{i},c{j}'])

                            #self.CjMap[f'f{i}c{j}']=0
                            cArr.append(self.ArrTable[f'f{i},c{j}'])

                            jR +=1
                        
                        if j>NVar+1 and j<c-1:
                            #la parte de los 0
                            v1= '1' if self.table0[parte0]+1==j else '0'
                            self.ArrTable[f'f{i},c{j}'] = LabelTable(text=v1)
                            
                            #self.CjMap[f'f{i}c{j}']=1 if self.table0[parte0]+1==j else 0
                        
                            cTable.add_widget(self.ArrTable[f'f{i},c{j}'])
                            cArr.append(self.ArrTable[f'f{i},c{j}'])
                           
                        if j == c-1:
                            v2= IRes[f'f{iR},c{jR+1}'].text
                            self.ArrTable[f'f{i},c{j}'] = LabelTable(text=v2)

                            #self.CjMap[f'f{i}c{j}']= int(IRes[f'f{iR},c{jR+1}'].text)
                            

                            cTable.add_widget(self.ArrTable[f'f{i},c{j}'])
                            cArr.append(self.ArrTable[f'f{i},c{j}'])
                if i == f -2:
                    if j==1:
                        fic1Label = LabelTable(text='Zj')
                        cTable.add_widget(fic1Label)
                    if j>1:
                        self.ArrTable[f'f{i},c{j}'] = LabelTable(text='0')

                        #self.CjMap[f'f{i}c{j}']= 0
                        

                        cTable.add_widget(self.ArrTable[f'f{i},c{j}'])
                        cArr.append(self.ArrTable[f'f{i},c{j}'])
                if i == f -1:
                    if j==1:
                        fic1Label = LabelTable(text='Cj-Zj')
                        cTable.add_widget(fic1Label)
                    if j>1 and j<c-1:
                        # cj -zj
                        v3 = self.fMap[0]                        
                        self.ArrTable[f'f{i},c{j}'] = LabelTable(text=f'{v3[j-2].text}')

                        

                        cTable.add_widget(self.ArrTable[f'f{i},c{j}']) 
                        cArr.append(self.ArrTable[f'f{i},c{j}'])                                             


                    #
                self.fMap[i]=cArr
                
                fTable.add_widget(cTable)
                #por que se pasa 2 veces el contador de i
            
            if i >1:
                iR +=1
                if parte0 != NRes-1:
                    parte0 += 1
                else:
                    parte0=0
            table.add_widget(fTable,1)
        
    

    def Maximizar(self):
        self.ids.generarTabla.disabled = True 
        newfMap = self.fMap        
        #Numero de filas y columnas de la tabla
        Nfilas = self.restricciones+3
        Ncolumnas = self.restricciones + self.variables + 2
        #escogemos la ultima fila
        codeUfila = newfMap[Nfilas]
        #escoger al mayor de la ultima fila
        UfilaArr =[]
        
        for i in codeUfila:
            uf = fr(i.text) 
            UfilaArr.append(uf)
        #se le suma uno mas por que los demas arrays tiene en la posicion 0 el numero que se cambia al final
        UfMayor = np.argmax(UfilaArr) +1         
        #escoger los pivotes que dependen del el valor mayor de la ultima fila en la posicion UfMayor 
        #pivotes va a contener la colunma de posicion UfMayor
        pivotes = []
        #reccoro cada fila sin tomar en cuenta las 2 primeras y las dos ultimas
        for i in newfMap:
            if i>1 and i<Nfilas-1:
                #reccoro cada columna escogiendo solo la de la posicion UfMayor que es el mayor
                for idx,j in enumerate(newfMap[i]):
                    if idx==UfMayor:
                        frac = fr(j.text)
                        pivotes.append(frac)
        #con los pivotes optenidos se pasa a dividir todas las filas
        # y guardarlos en un array para saber la columna Bi menor
        MapBiMenor={} 
        for i in newfMap:
            if i>1 and i<Nfilas-1:
                ArrBiMenor=[]
                for idx,j in enumerate(newfMap[i]):
                    col = fr(j.text)
                    division = col/pivotes[i-2]
                    ArrBiMenor.append(division)
                MapBiMenor[i-2]=ArrBiMenor
        #una ves separado y dividio cada fila para su pivote
        #tengo que buscar el menor de la ultima columna Ncolumnas o Bi guardandolo en un arreglo
        ArrBiMenor2 = []
        for i in MapBiMenor:
            for idx,j in enumerate(MapBiMenor[i]):
                #restamos 1 a las columnas por que hay una colunma que no esta incluida
                if idx == Ncolumnas-1:
                    ArrBiMenor2.append(j)
        #obtengo la posicion del menor pero como estamos trabajando en la tabla necesito aumentar las 
        # dos filas iniciales
        idxBiMenor= np.argmin(ArrBiMenor2)+2
        
        #ahora cambiamos los valores toda la fila por la fila de la posicion idxBiMenor
        #reccoremos cada fila del mapa princial excepto las 2 primeras y 2  ultimas
        # crear una arreglo para guardar la fila de Bi menor      
        filaBiMenor =[] 
        for i in self.fMap:
            if i>1 and i<Nfilas-1:
                if idxBiMenor == i:
                    for idx,j in enumerate(self.fMap[i]):
                        if idx ==0:
                            #reemplazamos el valor de la fila 0 con la columna mayor a la fila menor
                            fraction = fr(self.fMap[0][UfMayor-1].text)
                            numerador = fraction.numerator
                            denomina = fraction.denominator
                            value = numerador if denomina == 1 else fraction
                            j.text= str(value)
                            filaBiMenor.append(value)
                        else:
                            fraction = MapBiMenor[i-2][idx]
                            numerador = fraction.numerator
                            denomina = fraction.denominator
                            value = numerador if denomina == 1 else f'{numerador}/{denomina}'
                            j.text= str(value)
                            filaBiMenor.append(fraction)
        #ahora vamos a recorrer todas las filas para las iteracciones sin toca la fila que ya se cambio
        for i in self.fMap:
            if i>1 and i<Nfilas-1:
                if idxBiMenor != i:
                    for idx,j in enumerate(self.fMap[i]):
                        if idx !=0:
                            pivoNeg = -pivotes[i-2]
                            multBiPivo = filaBiMenor[idx]*pivoNeg
                            colIter= fr(j.text)
                            suma = multBiPivo + colIter
                            j.text= str(suma)
        #una vez calculado las filas se pasa a calcular Zj
        #zj es la multiplicacion de la columa 0  para sus filas y el resultado de cada columna se suma
        columna0=[]
        for i in self.fMap:
            if i>1 and i<Nfilas-1:
                for idx,j in enumerate(self.fMap[i]):
                    #print(filas)
                    if idx==0:
                        #este es el valor de la columna 0 
                        fract = fr(j.text)
                        columna0.append(fract)
        filasmultiplicadas ={}
        for i in self.fMap:
            if i>1 and i<Nfilas-1:
                arrfilasMul=[]
                
                for idx,j in enumerate(self.fMap[i]):
                    #print(filas)
                    if idx!=0:
                        fi = columna0[i-2]
                        fc = fr(j.text)
                        mult = fi*fc
                        arrfilasMul.append(mult)
                    else:
                        frac = fr(j.text)
                        arrfilasMul.append(frac)
                filasmultiplicadas[i-2]=arrfilasMul
        nZj=0
        for i in filasmultiplicadas:
            nZj+=np.array(filasmultiplicadas[i])
        Zj =nZj.tolist()
        #reeplazar en la tabla
        for i in self.fMap:
            if i==Nfilas-1:
                for idx,j in enumerate(self.fMap[i]):
                    #print(Zj,Zj[idx+1],j)
                    fraction =Zj[idx+1]
                    numerador = fraction.numerator
                    denomina = fraction.denominator
                    value = numerador if denomina ==1 else f'{numerador}/{denomina}' 
                    j.text = str(value)
            if i== Nfilas:
                for idx,j in enumerate(self.fMap[i]):
                    c0 = fr(self.fMap[0][idx].text)
                    filantepe = fr(self.fMap[i-1][idx].text)
                    resta = c0-filantepe
                    numerador = resta.numerator
                    denomina = resta.denominator
                    value = numerador if denomina ==1 else f'{numerador}/{denomina}' 
                    j.text=str(value)
            
            CjZj = self.fMap[Nfilas]
            arrCjZj = []
            for i in CjZj:
                fraction = fr(i.text)
                arrCjZj.append(fraction)
            a = np.array(arrCjZj)
            termina = (a<=0).all()
            if termina:
                self.show_alert_dialog()
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Fin de iteraciones",
                buttons=[
                    MDFlatButton(
                        text="Terminar",on_press=self.closeDIALOG
                    ),
                ],
            )
        self.dialog.open()
    def closeDIALOG(self,*arg):
        #MDFlatButton().disabled
        self.ids.maximiza.disabled = True
        self.dialog.dismiss(force=True)
        

            

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "400"
        return MainUI()

MainApp().run()