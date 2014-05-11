# -*- coding: utf-8 -*-
from operator import xor
from operator import or_
from operator import not_
from operator import and_
#==============================================================================
# Funcion auxiliar para Golomb
# Encuentra todas las rachas de una cadena.
# Entrada:
#     Cadena binaria en un "String" 
# Salida:
#     Diccionario con el numero de rachas y la posicion
#     de la forma {1: [7, 8, 9, 14], 2: [11, 13], 3: [2], 4: [6]}
#==============================================================================
def Rachas(cadena):
    
    rachas = {}    
    racha = 1
    
    i=0
    #todos si coinciden al principio y al final se ponen al final 
    #si la cadena es entera de 1 o de 0 se devuelve vacio
    while(cadena[0]==cadena[len(cadena)-1]):
        if(i>len(cadena)):
            return dict()
        cadena = cadena[1:]+cadena[0]
        i+=1
        
    #anadimos un 0 o 1 al final, al contrario de lo que acabe para que cuente
    #la ultima racha
    if(cadena[len(cadena)-1]=="1"):
        cadena+="0"
    else:
        cadena+="1"

    for i in range(0,len(cadena)-1):
        if(cadena[i]==cadena[i+1]):
            racha+=1
        else:
            try:
                rachas[racha].append(i)
            except:
                rachas[racha]=[i]
            #rachas[i]=racha
            racha = 1 

    return rachas

#==============================================================================
# Funcion auxiliar de Golomb
# Dadas dos cadenas (String) en binario
# Busca las diferencias de 0 y 1 en una cadena
# Entrada:
#     Cadena1: "0101010101"
#     Cadena2: "1010101010"
# Salida:
#     Diferencia: Entero con la diferencia de posiciones en las que no coinciden
#    los 0 y 1
#==============================================================================

def Hamming(cadena1,cadena2):
    
    #assert(len(cadena1)==len(cadena2))

    diferencia = 0    
    for i,j in zip(cadena1,cadena2):
        if(i!=j):
            diferencia+=1    
            
    return diferencia

#==============================================================================
# Dada una cadena String nos dice si cumple los postulados de Golomb
# Entrada:
#     cadena: "0101010101"
# Salida:
#     [True,True,True] refiriendose al primer postulado, segundo postulado
#     y tercer postulado respectivamente
#==============================================================================

def Golomb(cadena):
    
    resultado = [True, True, True]    
    
    zeros = cadena.count("0")
    unos = cadena.count("1")
    
    if(abs(zeros-unos)>1):
        resultado[0]=False
    
    rachas = Rachas(cadena)
    numrachas = rachas.keys()

    #si la cadena no esta formada por un solo numero
    if(rachas):
        for i in range(0,len(numrachas)-1):
            if(abs(numrachas[i]-numrachas[i+1])!=1):
                resultado[1]=False
                break;
            if(len(rachas[numrachas[i]])!=2*len(rachas[numrachas[i+1]])):
                if(len(rachas[numrachas[i]])!=1 and len(rachas[numrachas[i+1]])!=1):
                    resultado[1]=False
                    break;
    else:
        resultado[1]=False
    
  
    
    cadena2 = cadena[1:]+cadena[:1]
    ham = Hamming(cadena,cadena2)    
    for i in range(2,len(cadena)-1):
        cadena2 = cadena[i:]+cadena[:i]
        if(ham!=Hamming(cadena,cadena2)):
               resultado[2]==False       
    
    return resultado
  


#==============================================================================
# Lineal Feedback shift register
# Entrada: 
#     Lista con coeficientes [1,0,1,0...]
#     Lista con semilla [1,1,0,1...]
#     Longitud: entero con la cadena a generar
# Salida:
#     Lista con secuencia generada
#     String con secuencia generada
# Excepciones:
#     La semilla ha de ser del mismo tamano que la lista
#==============================================================================

def LFSR(coef,sem,longitud):
    
    assert(len(coef)==len(sem))
        
    fin_cadena = ""
    fin_lista = []
    
    #Por cada caracter a generar
    for k in xrange(0,longitud):
        #reiniciamos el feedback
        sj = 0
        #por cada coeficiente del polinomio
        for i in xrange(0,len(coef)):
            #se multiplica (and) y se hace el xor con la anterior sj
            a = sem[i]*coef[i]
            sj = xor(sj,a)
        #se anade la semilla a la cadena
        fin_cadena += str(sem[len(sem)-1])        
        fin_lista.append(int(sem[len(sem)-1]))
        #se anade al principio
        sem = [sj]+sem
        # y se desplaza la semilla
        sem = sem[0:len(sem)-1]

 
    return fin_cadena,fin_lista


#==============================================================================
# Non Lineal Feedback Shift Registrer
# Entrada:
#     f: Lista con los coeficientes de los monomios: [[0,1],[1,1]]
#     s: Semilla del mismo tamano que la lista
#     k: Secuencia a generar
# Salida:
#     Lista de cadena generada
#     String de cadena generada
# Excepciones:
#     La semilla tiene que ser del mismo tamano que los monomios
# No contempladas:
#     Tienen que tener el mismo numero de variables todas los monomios
#==============================================================================

def NLFSR(f, s, k):

    assert(len(f[0])==len(s))

    fin_cadena = ""
    fin_lista = []
    
    #generamos K numeros    
    for _ in range(0,k): 
        #f monomios
        sj = 0
        for i in f:
            r = 1
            #j variables
            for j,sem in zip(i,s):
                r += sem*j
            r = r%2
            sj = xor(sj,r)
            
        fin_cadena += str(sj)
        fin_lista.append(sj)
        s = [sj]+s
        s = s[0:len(s)-1]

    return fin_cadena,fin_lista
    

#==============================================================================
# Generador Geffe
# Entrada:
#     Tres polinomios:
#         coef1,s1
#         coef2,s2
#         coef3,s3
#         del tipo [1,0,1],[0,0,1]
#     Longitud de la cadena a generar
# Salida:
#     Cadena de String generada
#     Lista de enteros generada
#==============================================================================
    
def geffe(coef1, s1, coef2, s2, coef3, s3, l):
    
    #creamos tres LFSR con los coeficientes
    c1, l1 = LFSR(coef1, s1, l)
    c2, l2 = LFSR(coef2, s2, l)
    c3, l3 = LFSR(coef3, s3, l)

    final_cadena = ""
    final_lista = []   
    
    #y se realiza la "fusion"
    #x1 es el and de lfsr1 y lfsr2
    #x2 es el and de lfsr2 y lfsr3
    #f es el xor del xor de x1 y x2 con x3
    for i,j,k in zip(l1,l2,l3):
        x1 = i*j; x2= j*k; x3 = k;
        f = xor(xor(x1,x2),x3)
        final_cadena += str(f)
        final_lista.append(f)
    
    return final_cadena,final_lista
    
#==============================================================================
# Algoritmo de Berlekamp-massey para determinar el polinomio que genera
# una cadena. 
# Entrada: 
#     la cadena
# Salida:
#     L la complejidad
#     C el polinomio
#==============================================================================
def BerlekampMassey(s):

    C = [1]
    L = 0
    m = -1
    B = [1]
    N = 0
    T = []
    l = 1
    while(N<len(s)):
        d = 0
                
        for i in range(0,L+1):
            d+=C[i]*s[N-i]
        d = d%2
        
        if d == 1:
            T=C
            ####C(D) = C(D)+B(D)*x^(n-m)
            D = [0]*(N-m)+B #B(D) + x^(n-m)
            if(len(D)>len(C)): #ajuste de indices
                C = C+([0]*(len(D)-len(C)))
            for i in range(0,len(D)): 
                C[i] = (C[i]+D[i])%2
            if(L<=N/2):
                L=N+1-L
                m=N
                B=T
                l=1
            else:
                l+=1
        else:
             l+=1

        N = N+1
    
    return L,C

#==============================================================================
# Funcion de encriptacion de un texto utilizando geffe
# Entrada:
#     Texto a encriptar
#     Parametros para geffe (iguales al anterior)
# Salida
#     Mensaje en lista
#     Mensaje en cadena
# Procedimiento:
#     Se realiza el xor entre el texto y el NLFSR generado por geffe
#==============================================================================

def Encriptar(txt, coef1, s1, coef2, s2, coef3, s3, l):
    result_c, result_l = geffe(coef1, s1, coef2, s2, coef3, s3, l)

    msg_lista = []
    msg_cadena = ""
    
    for i,j in zip(txt,result_l):
        msg = xor(int(i),j)
        msg_lista.append(msg)
        msg_cadena += str(msg)
        
    return msg_lista, msg_cadena
