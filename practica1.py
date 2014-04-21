# -*- coding: utf-8 -*-
import random
from math import sqrt
from math import ceil

def gcd(a,b):
    
    if(b>a):
        a,b=b,a 
        
    if(b==0):
        return [a,1,0]
        
    x2,x1,y2,y1=1,0,0,1
    
    while(b>0):
        q=a/b
        r=a-q*b
        x,y=x2-q*x1,y2-q*y1
        a,b,x2,x1,y2,y1=b,r,x1,x,y1,y

    return [a,x2,y2]
    
def inverso(a,b):

    d,u,v = gcd(a,b)    

    if(d!=1):
        return False;
    else:
        return v
    
    return None

def exponenciacion(a,k,n):
    
    b = 1
    kbin = '{0:b}'.format(k)[::-1]
    A = a    
    
    if(k==0):
        return b
    
    if(kbin[0]==1):
        b=a

    for i in kbin:
        if(i=='1'):
            b = multiplicacion(A,b)%n         
        A = multiplicacion(A,A)%n        
        
    return b
    
def MillerRabinStep(n,m,l):      
 
    alea = random.randint(2,n-2)
    a = exponenciacion(alea,m,n)
    
    if(a==1 or a==-1%n):
        return True
    else:
        for i in range(1,l-1):
            a = exponenciacion(a,2,n)
            if(a==-1%n):
                return True
            elif(a==1):
                return False
        return False

    return False

def MillerRabin(n,k):
    
    if(n%2==0):
        return False
    
    m, l = n-1, 0
    while (m%2==0):
        l+=1; m/=2
    for i in range(1,k):
        if(not MillerRabinStep(n,m,l)):
            return False

    return True


def EnanoGigante(b,a,p):
    
    m = long(sqrt(p-1)+0.99)
    
    table = {}
    for i in range(0,m):
        table[pow(a,i) % p] = i
    
    ap = inverso(a,p)
    am = exponenciacion(ap,m,p)
    y = b

    for i in range(0,m-1):
        try:
            j = table[y]
            return i*m+j
        except:
            y = (y*am) % p
    

    return None

def Jacobi(a,n):
    
#    assert(n>2)
#    assert(a<n) 
    
    
    if(a==0):
        return 0
    if(a==1):
        return 1
        

    m, e = a, 0
    while (m%2==0):
        e+=1; m=m/2
        
    if(e%2==0):
        s = 1
    elif( (n-1)%8==0 or (n-7)%8==0):
        s = 1
    elif( (n-3)%8==0 or (n-5)%8==0):
        s = -1
    if( (n-3)%4==0 and (m-3)%4==0):
        s = -s
    
    n1 = n % m        
    if(m==1):
        return s
    else:
        return s*Jacobi(n1,m)
    
    return None
    

def residuosCuadrados(a,p):
    
    r=0
    n = 0
    
    if(Jacobi(a,p)==1):
        for i in xrange(0,p):
            if(Jacobi(i,p)==-1):        
                n=i
                pass
            
        s, u = p-1, 0
        while (s%2==0):
            u+=1; s=s/2
        
        if(u==1):
            r = pow(a,(p+1)/4)%p
        if(u>1):
            r = pow(a,(s+1)/2)%p
            b = pow(n,s)%p
            j=0
            while(j<=u-2):
                base = (inverso(a,p)*pow(r,2))%p
                exp = pow(2,u-2-j)%p
                if(pow(base,exp)%p==(-1%p)):
                    r = (r*b)%p
                b = pow(b,2)%p
                j+=1
    else:
        return False


    return r,p-r
    

def teoremaChino(a,n,p,q):


    r, r2 = residuosCuadrados(a,p)
    s, s2 = residuosCuadrados(a,q)
    
    Ap = (q * inverso(a,p)) %n
    Aq = (p * inverso(a,q)) %n
    
   
    x = ((Ap*r)+(Aq*s))%n
    y = ((Ap*r2)-(Aq*s2))%n

    return [x,-x%n,y,-y%n]   
    
def factorizacionFermat(n):
    
    x = ceil(sqrt(n))
    cuadradoperfecto = False    
    
    while(not cuadradoperfecto):
        cp = pow(x,2)

        if(sqrt(cp-n)%1==0):
            cuadradoperfecto = True
        else:
            x+=1;
            
    cp = cp%n
    cp = sqrt(cp)
    return [x,cp]
    
    
def factorizacionPollard(n,iters):
    a,b = 2,2
    d = 1
    
    for _ in range(0,iters):
        a,b = long(pow(a,2)+1)%n,long(pow(b,2)+1)%n
        b = long(pow(b,2)+1)%n
        d,u,v = gcd((a-b),n)
        if(d>1 and d<n):
            return [d,True]

    return [d,False]
