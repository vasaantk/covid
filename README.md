# covid
Scripts to plot countries' covid-19 data
```
covid.py plots the number of covid cases for user defined countries. 
                                                                     
Usage:                                                               
          -->$ covid.py south\ africa singapore hubei,\ china        
          -->$ covid.py new\ zealand mali --diff                     
                                                                     
You can also obtain the number of cases relative to the population by
providing an input.txt file with the following format:               
                                                                     
# state (if applicable), country, population                         
south africa, 57.78e6                                                
victoria, australia, 6.359e6                                         
tasmania, australia, 515000                                          
united kingdom, 66.65e6                                              
                                                                     
          -->$ covid.py input.txt                                    
          -->$ covid.py input.txt --diff 
```
