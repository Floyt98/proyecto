from __future__ import division
import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")
import os,codecs,nltk,shutil,glob,numpy,re,pandas
nltk.download('averaged_perceptron_tagger')

def creaClases(tamano):
    novelasXclase=3
    etapas=2 #3 para 3 etapas
    clase=[]
    for etapa in range(1,etapas+1):
        clase+=[etapa]*int(tamano)*novelasXclase
        
    return clase
    
def crearModelosXautor(ruta,tamanos,tipo,n):
    os.chdir(ruta)
    lista_autores=os.walk('.').__next__()[1]
    for autor in lista_autores:
        os.chdir(autor) ##########################################entra autor
        for tamano in tamanos: 
            os.chdir(tamano) ####################################entra tamano 
            clase=[]
            tokens=[]
            clase=creaClases(tamano) #la longitud de clase es el numero de instancias       
            c=0
            texto=open('col'+str(n)+'gramas'+tipo+autor+tamano+'.txt','r')
            lista=texto.readlines()
            texto.close()
            for p in lista:
                tokens.append(p[0:-1])
            columnas=len(tokens)
            matriz=numpy.zeros((len(clase),columnas))
            diccionario={}
            cont=0
            for item in tokens:
                diccionario[item]=cont
                cont=cont+1
            print ("creando VSM del autor :",autor)    
            lista_novelas=os.walk('.').__next__()[1]
            for novela in lista_novelas:
                os.chdir(novela) ##############################entra novelas
                lista_documentos=os.walk('.').__next__()[1]
                for documento in lista_documentos:
                    os.chdir(documento) #####################entra documentos
                    texto=open(str(n)+'gramas.txt','r')
                    lista=texto.readlines()
                    texto.close()
                     #ESTE ES EL TOTAL DE COLUMNAS DE LA MATRIZ
                    ngramas=[]
                    for p in lista:
                        ngramas.append(p.replace('\n','').split(' '))
                    aux=len(ngramas)
                    for x in range(aux):
                        aux=ngramas[x][0]
                        y=diccionario[aux]
                        matriz[c][y]=int(ngramas[x][1])                    
                    c=c+1
                    os.chdir('..') ###########################sale documentos
                os.chdir('..') ##################################sale novelas
            #auxmatriz=numpy.c_[matriz,clase]
            #tokens.append('clase')
            df=pandas.DataFrame(matriz,  columns=tokens)
            #numpy.savetxt('vsm'+str(N)+'gramas'+tamano+tipo+'.txt',auxmatriz,fmt='%1.1f')
            print ('sumando frecuencias y ordenando descendente')
            suma=df.sum(axis=0,)
            df=df.append(suma,ignore_index=True)
            df=df.reindex(sorted(df.columns, key=lambda x: df[x][len(clase)],reverse=True), axis=1)
            clase.append(0)            
            df['clase']=clase
            df=df[:-1]
            df.to_csv('vsm'+str(n)+'gramas'+tipo+autor+tamano+'.csv',index=False)
            os.chdir('..') ########################################sale tamano 
        os.chdir('..') ############################################entra autor

def ngramasXnovelas(ruta,tamanos,tipo,n):
    os.chdir(ruta)
    lista_autores=os.walk('.').__next__()[1]       
    for autor in lista_autores:
        os.chdir(autor) ##########################################entra autor
        for tamano in tamanos: 
            os.chdir(tamano) ####################################entra tamano 
            total=[]
            tokens=[]
            salida=[]
            resumen=open(str(n)+'gramas'+tipo+autor+tamano+'.txt','w')    
            lista_novelas=os.walk('.').__next__()[1]
            for novelas in lista_novelas:
                print ("el directorio actual es  ",os.getcwd())
                os.chdir(novelas) ##############################entra novelas
                lista_documentos=os.walk('.').__next__()[1]
                for documento in lista_documentos:
                    os.chdir(documento) #####################entra documentos
                    texto=open(str(n)+'gramas.txt','r')
                    lista=texto.readlines()
                    texto.close()
                    for p in lista:
                        aux=p.find(' ')
                        if aux!=-1:
                            tokens.append(p[0:aux]+'\n')
                    print (autor,' ',novelas,' gramas ',len(lista))
                    #salida.append(autor+'\t'+documento+'\t'+str(len(lista))+'\t'+'acumulado\t'+str(len(tokens))+'\t'+str(n)+'gramas\n')
                    lista=list()
                    os.chdir('..') ###########################sale documentos
                os.chdir('..') ##################################sale novelas
            total=list(set(tokens))
            #print 'total de ngramas== ',len(tokens),' ngramas diferentes== ',len(total)
            arch=open('col'+str(n)+'gramas'+tipo+autor+tamano+'.txt','w')
            arch.writelines(total)
            arch.close()
            salida.append('vocabulario total del autor '+autor+'\t'+str(len(total))+'\t'+str(n)+'gramas\n')
            tokens=list()
            total=list()
            resumen.writelines(salida)
            resumen.close()
            os.chdir('..') ########################################sale tamano 
        os.chdir('..') ############################################entra autor

def creaMuestras(ruta,tamanos):
    os.chdir(ruta)
    lista_autores=os.walk('.').__next__()[1]
    for autor in lista_autores:
        os.chdir(autor)
        print ("el directorio actual es  ",os.getcwd())
        lista_novelas=[]
        df=pandas.read_csv("configuracion.csv",dtype={'Etiqueta':'str'})
        for index, row in df.iterrows():
            if row["Etiqueta"]!='0':
                lista_novelas.append((row["Nombre_Novela"],row["Etiqueta"]))
        #lista_novelas=glob.glob('x*.*')
        for tamano in tamanos:
            if os.path.exists(tamano):
                shutil.rmtree(tamano)
            os.makedirs(tamano)
            muestras=[]    
            for novelas in lista_novelas:
                lista=[]
                print ('procesando ',autor, 'novela ',novelas)
                #cadena=novelas.split(".")
                file=codecs.open(novelas[0]+'.txt','r','utf-8',errors='replace')
                lista=file.readlines()
                file.close()
                sentencias=int(len(lista)/int(tamano))
                nodocumentos=int(len(lista)/sentencias)
                muestras.append(novelas[0]+' '+str(nodocumentos)+'\n')
                if os.path.exists(novelas[0]):
                    shutil.rmtree(novelas[0])
                os.chdir(tamano)                            
                os.makedirs(novelas[0])            
                os.chdir(novelas[0])
                indice=0
                for x in range(0,nodocumentos):
                    tokens=list()
                    for y in range(0,sentencias):
                        tokens.append(lista[indice])
                        indice=indice+1
                    arch=codecs.open(novelas[0]+'_'+str(x+1)+'.txt','w',encoding="utf-8")
                    arch.writelines(tokens)
                    arch.close()
                os.chdir('..')
                os.chdir('..')
            os.chdir(tamano) #entrar a tamano de muestra 
            escribe=open('muestras'+autor+tamano+'.txt','w')
            escribe.writelines(muestras)
            escribe.close()    
            os.chdir('..') #salir a tamano de muestra 
        os.chdir('..')

def uneNgramas(archivo):
    file=open(archivo,'r')
    lista=file.readlines()
    file.close()
    print ('procesando el archivo',archivo)
    x=int(archivo[0]) #reemplaza espacios por guiones bajos
    juntos=list()
    for p in lista:
        temp=p.replace(' ','_',x-1)
        juntos.append(temp)                        
    os.remove(archivo)
    escribir=open(archivo,'w')
    escribir.writelines(juntos)
    escribir.close()
    
def creaNgramas(ruta,tamanos,tipo,n,frecuencia):
    if tipo=='POS':
        creaTAGs(ruta,tamanos)
    os.chdir(ruta)
    lista_autores=os.walk('.').__next__()[1]
    for autor in lista_autores:
        os.chdir(autor)
        print ("generando n-gramas del autor ",autor)
        for tamano in tamanos:
            os.chdir(tamano)            
            lista_novelas=os.walk('.').__next__()[1]
            for novelas in lista_novelas:
                os.chdir(novelas)
                lista_documentos=glob.glob('*.txt')
                for documento in lista_documentos:
                    print ('procesando novela ',documento)
                    cadena=documento.split(".")        
                    if os.path.exists(cadena[0]):
                        shutil.rmtree(cadena[0])
                    os.makedirs(cadena[0])                      
                    actual=os.getcwd()+'\\'+documento        
                    os.chdir(cadena[0])       
                    shutil.copy(actual,os.getcwd())
                    longitud=' -n'+str(n)
                    frec=' -f'+str(frecuencia)+' '
                    if tipo=='PAL'or tipo=='POS':
                        cadena='C:\\ngramadores\\ngramtool\\text2ngram'+longitud+frec+documento+'>>'+str(n)+'gramas.txt'
                        os.system(cadena)
                        if n!='1':
                            uneNgramas(str(n)+'gramas.txt')                 
                    else: #en caso de que sea caracter se requiere un parámetro extra
                        cadena='C:\\ngramadores\\ngramtool\\text2ngram -c'+longitud+frec+documento+'>>'+str(n)+'gramas.txt'
                        os.system(cadena)                          
                    os.remove(documento)
                    os.chdir('..')
                os.chdir('..')
            os.chdir('..')
        os.chdir('..')

def creaTAGs(ruta,tamanos):
    os.chdir(ruta)
    lista_autores=os.walk('.').__next__()[1]
    for autor in lista_autores:
        os.chdir(autor) ##########################################entra autor
        for tamano in tamanos: 
            os.chdir(tamano) ####################################entra tamano 
            print ("el directorio actual es  ",os.getcwd())
            #directorio=glob.glob('*.txt')
            lista_novelas=os.walk('.').__next__()[1]
            for novela in lista_novelas:
                print ('preprocesando novela ',novela)
                os.chdir(novela) ##############################entra novelas
                directorio=glob.glob('*.txt')
                for documento in directorio:
                    file=codecs.open(documento,"r","utf8")
                    lista=file.read()
                    file.close()
                    tokens=list()
                    tags=list()
                    tokens=nltk.word_tokenize(lista)
                    print ('creando POS del autor ',autor, 'novela ',documento)
                    tags=nltk.pos_tag(tokens)
                    tokens=list()
                    for termino in tags:
                        if re.match(r'^[A-Z]|[A-Z]$',termino[1]):
                            tokens.append(termino[1])
                    cadena=' '.join(tokens)
                    os.remove(documento)        
                    escribir=open(documento,'w')
                    escribir.writelines(cadena)
                    escribir.close()
                os.chdir('..') ##############################entra novelas
            os.chdir('..') ####################################entra tamano 
        os.chdir('..') ############################################sale autor


if __name__ == '__main__':
    corpus='D:\Residencia\Proyecto\Corpus11autores'
    tipoNgrama='PAL'
    longitudNgrama=2
    frecuencia=6
    #tamano muestra 1=completa 2=media 3=tercio 4=cuarto    
    tamanoMuestra=['1','2','3','4','5','6']    
    creaMuestras(corpus,tamanoMuestra)    
    creaNgramas(corpus,tamanoMuestra,tipoNgrama,longitudNgrama,frecuencia)    
    ngramasXnovelas(corpus,tamanoMuestra,tipoNgrama,longitudNgrama)
    crearModelosXautor(corpus,tamanoMuestra,tipoNgrama,longitudNgrama)
    