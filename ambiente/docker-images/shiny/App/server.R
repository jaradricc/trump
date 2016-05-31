#!/usr/bin/env Rscript





library(shiny)
library(RJSONIO)
library(ggplot2)
library(dplyr)
library(wordcloud)
library(tidyr)

#############################
# LECTURA DE DATOS HASTAGS
############################

#path <- '~/Poyectos_local/ITAM/DPA/APP_SHINY'
#path <- '/Users/omardiaz/Dropbox/ITAM_Master/dpa/proyecto_final/Shiny_DEF'
path <- '/datalake'

file <- paste(path,'/2016523top_hashtags.json',sep="")
json_file <- fromJSON(file)

json_file <- lapply(json_file, function(x) {
  x[sapply(x, is.null)] <- NA
  unlist(x)
})

data<-do.call("rbind", json_file)
data<-as.data.frame(data)
data_hashtags<- cbind(rownames(data), data)
rownames(data_hashtags) <- NULL
colnames(data_hashtags) <- c("hashtag","total")

file <- paste(path,'/2016523top_users.json',sep="")
json_file <- fromJSON(file)
json_file <- lapply(json_file, function(x) {
  x[sapply(x, is.null)] <- NA
  unlist(x)
})

data_users<-do.call("rbind", json_file)
data_users<-t(data_users)
data_users<-as.data.frame(data_users)

###################################
# LECTURA DE DATOS SERIES DE TIEMPO
###################################
file <- paste(path,'/dates_prueba.csv',sep="")
dates_prueba<-read.table(file,header=T,sep=";")

dates_prueba$month <- substr(dates_prueba$DATE, 1, 3)
dates_prueba$day <- substr(dates_prueba$DATE, 5, 6)
dates_prueba$year <- substr(dates_prueba$DATE, 8, 11)

dates_prueba$month<-sapply(dates_prueba$month,function(x) grep(paste("(?i)",x,sep=""),month.abb))

dates_prueba$month<-paste("0",dates_prueba$month,sep="")

dates_prueba$newdate<-paste(dates_prueba$year,dates_prueba$month,
                            dates_prueba$day,sep="-")

dates_prueba$newdate<-as.Date(dates_prueba$newdate,"%Y-%m-%d")





## SHINY SERVER FUNCTION
shinyServer(function(input,output){

  #############################
  # GRAFICA DE WORDCLOUD
  ############################

  output$hashtags<- renderPlot({
    data_hashtags <- arrange(data_hashtags, desc(total))
    data_w <- data_hashtags[1:input$num_hashtags,]
    data_w$hashtag<-paste("#",data_w$hashtag,sep = "")
    wordcloud(data_w$hashtag,data_w$total,
              scale=c(5,.7),
              min.freq=2,
              ordered.colors=T,
              colors=colorRampPalette(brewer.pal(9,"Set1"))(nrow(data_w)))
  })

  #############################
  # GRAFICA DE USERS
  ############################

  output$users <- renderPlot({
    top <- data_users[1:input$num_users,]
    ggplot(top, aes(user_name, total)) +
      geom_bar(stat = "identity")+coord_flip()
  })

  #############################
  # GRAFICA DE SERIES DE TIEMPO
  ############################

  output$tseries <- renderPlot({

    dates_p<-filter(dates_prueba, newdate >= as.character(input$dateRange2[1]) & newdate <= as.character(input$dateRange2[2]))

    dates_p %>%
      tidyr::gather(k, v, Tweet, Retweet) %>%
      ggplot(aes(newdate)) +
      geom_ribbon(aes(ymin=0, ymax=v,fill = k),alpha=0.5)+
      geom_line(aes(y=v, color=k), size=1) +
      scale_fill_manual(name='', values=c('Tweet'=rgb(.1,.9,.9),
                                          'Retweet'='navyblue')) +
      scale_color_manual(name='', values=c('Tweet'=rgb(.1,.9,.9),
                                           'Retweet'='navyblue')) +
      guides(color=element_blank())+
      xlab("FECHA")+ylab("CANTIDAD")
  })




})


##############################
