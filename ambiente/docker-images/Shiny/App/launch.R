#!/usr/bin/env Rscript

setwd("/root")
#install.packages("shiny")
#install.packages("RJSONIO")
#install.packages("ggplot2")
#install.packages("dplyr")
#install.packages("wordcloud")
#install.packages("tidyr")
#install.packages("shinydashboard")
#install.packages("leaflet")

shiny::runApp(port=6403,host="172.17.0.2")
