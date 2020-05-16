import xmlrpc.client
import datetime
s = xmlrpc.client.ServerProxy('http://localhost:8000')

continuar = True
while continuar:

    idOp = 0
    num1 = 0
    num2 = 0

    print ("Calculadora Basica RPC")
    print ("\t 1. Suma")
    print ("\t 2. Resta")
    print ("\t 3. Multiplicacion")
    print ("\t 4. Division")

    idOp = int(input("Ingrese el número de la operación que desea realizar:\n"))

    if idOp>0 and idOp<5:
            num1 = int(input("\tIngrese el primer número de la operación: \n"))
            num2 = int(input("\tIngrese el segundo número de la operación: \n"))

            if idOp == 1:
                print ("\tResultado= ", s.add(num1,num2))
            elif idOp == 2:
                print ("\tResultado= ", s.sub(num1,num2))
            elif idOp == 3:
                print ("\tResultado= ", s.mult(num1,num2))
            elif idOp == 4:
                if num2 == 0:
                    print ("\tEl divisor debe ser diferente de 0.\n")
                else:
                    print ("\tRESULTADO: ", s.div(num1,num2))
            else:
                print("idOp invalida \n")
