from funs import *
from Ant import Ant
import time
import pickle
from os import path

dataM=readData('Input/solomon_r101.txt')

distM=createDistanceMatrix(dataM)

#print(dataM[1])

phiM1=createPheromoneMatix(size=len(distM),distance=1888)
feasLocIN1=len(distM)*[0]

phiM2=createPheromoneMatix(size=len(distM),distance=1888)
feasLocIN2=len(distM)*[0]


#nnSearch(0,distM,dataM)
#print(dataM[1])

vehicleNumber=60

ant0=Ant(vehicleCount=vehicleNumber,dataM=dataM)
bestSolution=ant0.calculate(dataM,distM,phiM1,feasLocIN1,1)

#getting ready phi matrix file
TF_Path=path.relpath('Output/Phi.txt')
            
tf=open(TF_Path,'w')
tf.write('phi matrix:\n\n')
tf.close()
#phi m write


iteration=0
while iteration <500:
    #print('iteration number',antCount
    
    #solution 1 is looking for a valid solution with fewer number of vehicles
    ant1=Ant(vehicleCount=vehicleNumber-1,dataM=dataM)
    solution1=ant1.calculate(dataM,distM,phiM1,feasLocIN1,1)
       
    if solution1['visitedCount']==100:
        vehicleNumber-=1
        
        phiM2=createPheromoneMatix(size=len(distM),distance=1888)
        #feasLocIN2=len(distM)*[0]


        #update pheromones
        for vehicle in solution1['vehicles']:
            for index in range(0,len(vehicle['tour'])-1):
                fromLoc=vehicle['tour'][index]
                toLoc=vehicle['tour'][index+1]
                phiM1[fromLoc][toLoc]=(1-0.1)*phiM1[fromLoc][toLoc]+0.1/solution1['distance']
            
        bsChange=False
        if bestSolution['vehicleCount']>solution1['vehicleCount']:
            bestSolution=solution1
            bsChange=True
        elif bestSolution['vehicleCount']==solution1['vehicleCount'] and bestSolution['distance']>solution1['distance']:
            bestSolution=solution1
            bsChange=True
        
        if bsChange==True:

            print('**********')
            print('The best solution currently is:')
            #for index,vehicle in enumerate(solution['vehicles']):
            #    print('Vehicle',index+1,'\ttour:',vehicle['tour'])
            #    print('')
            print('Vehicle count is:',solution1['vehicleCount'])
            print('Visited count is:',solution1['visitedCount'])
            print('Distance traveled is:',solution1['distance'])
            print('Current Iteration is:',iteration)
            print('')
            print('')
            #time.sleep(2)
    

    #solution two is looking for a shorter distance
    ant2=Ant(vehicleCount=vehicleNumber,dataM=dataM)
    solution2=ant2.calculate(dataM,distM,phiM2,feasLocIN2,1)
    
    if solution2['visitedCount']==100:

        #update pheromones
        for vehicle in solution2['vehicles']:
            for index in range(0,len(vehicle['tour'])-1):
                fromLoc=vehicle['tour'][index]
                toLoc=vehicle['tour'][index+1]
                phiM2[fromLoc][toLoc]=(1-0.1)*phiM2[fromLoc][toLoc]+0.1/solution2['distance']
            
        bsChange=False
        if bestSolution['distance']>solution2['distance']:
            bestSolution=solution2
            bsChange=True
        
        if bsChange==True:
            print('**********')
            print('The best solution currently is:')
            #for index,vehicle in enumerate(solution['vehicles']):
            #    print('Vehicle',index+1,'\ttour:',vehicle['tour'])
            #    print('')
            print('Vehicle count is:',solution2['vehicleCount'])
            print('Visited count is:',solution2['visitedCount'])
            print('Distance traveled is:',solution2['distance'])
            print('')
            print('')
            #time.sleep(2)
            
            tf=open(TF_Path,'a')
            for ph in phiM1:
                for ph2 in ph:
                        tf.write(str(ph2))
                        tf.write('\n')
                tf.write('\n\n')
            tf.close()
            
            #pickle to save best solution to play with somewhere else
            #file_name='best_solution'+str(iteration)
            #fileObject =open(file_name,'wb')
            #pickle.dump(bestSolution,fileObject)
            #fileObject.close()
            
    iteration+=1

print('we are done')



BS_Path=path.relpath('Output/BestSolution.txt')
txtFile = open(BS_Path, 'w')
txtFile.write('Vehicle Log\n\n')
txtFile.close()

txtFile = open(BS_Path,"a")
for index,vehicle in enumerate(bestSolution['vehicles']):
    txtFile.write('Vehicle\t')
    txtFile.write(str(index+1))
    txtFile.write('\ttour:\t')
    txtFile.write(str(vehicle['tour']))
    txtFile.write('\n')
txtFile.close()


