# generate-network-project

This is a project for the project course (1DL507 and 1DL505) at Uppsala university. 

Overall, we worked on generating synthetic population registry data for one year but also coherent data for multiple years. 

Furthermore, we created different layers for a social network based first on our synthetic data, but then also on the swedish registry data (SCB). 

We created the basis fo data creation and understanding of all variables together as a group. But overall the group was mainly divided the following way. 

## Synthetic Data: 
Ludvig, (Xenia)

This code generates data for one or several years for coherent family, work and education development through time. 


## Family Layer: 
Inga

There are two version for this code, both generating the family relations from registry data for the social network. One generating the family layer for one year, using the variables available to us in the swedish registry day and/or present in the synthetic data. 
The other is using the same data for several years, creating the layers over multiple years, including the information from previous years into the current data. This code is still needing to be more optimisied in terms of running time on a large data set, but it is fully functional. 

## Work Layer: 
Ruvimbo

This code creates the layer regarding work relations using two approaches. As the years are independent, it can simply be used for any year to create a layer for the social network from it. 

## Education Layer:
Ruvimbo

This code creates a layer linking individuals based shared educational experiences. As the years are independent, it can simply be used for any year to create a layer for the social network from it. 
