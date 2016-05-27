#!/usr/bin/env Rscript

library(shiny)
library(shinydashboard)
library(leaflet)


header <- dashboardHeader(
  title = "TWITTER DASHBOARD"
)



body<-dashboardBody(

  #############################
  # GRAFICA DE SERIES DE TIEMPO
  ############################


  fluidRow(
    box(
      title = "Date Input", status = "warning",
      dateRangeInput('dateRange2',
                     label = paste('Selecciona un intervalo'),
                     start = Sys.Date() - 3, end = Sys.Date() + 3,
                     min = "2016-05-01", max = Sys.Date() - 1, format = "yyyy-mm-dd",
                     startview = 'year', weekstart = 1
      )
    ),
    box(title = "Time Series", status = "primary", plotOutput("tseries", height = "300px"))

  ),


  #############################
  # GRAFICA DE USERS
  ############################
  fluidRow(
    box(title = "Users Histogram", status = "primary", plotOutput("users")),

    box(
      title = "Inputs", status = "warning",
      "Cantidad de publicaciones por usuario", br(), "Nos permitira identificar BOTS",
      sliderInput(inputId="num_users",
                  label="Elige un TOP de usarios que observar",
                  value = 5, min=3, max=15)
    )

  ),

  #############################
  # GRAFICA DE WORDCLOUD
  ############################

  fluidRow(


    box(
      title = "Hashtags Inputs", status = "warning",
      "Muestra los Hashtags mas populares", br(), "Motor de busqueda Trump, trump, Trump2016",
      sliderInput(inputId="num_hashtags",
                  label="Elige un numero de Hashtags",
                  value = 5, min=3, max=20)
    ),

    box(title = "WordCloud", status = "primary", plotOutput("hashtags"))

  )



)



dashboardPage(
  header,
  dashboardSidebar(disable = TRUE),
  body
)
