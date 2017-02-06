source('header.R')

cat("Loading testing data ...\n")
load("test_data_final.rdata")
levels(test_data[, 'user_country'])[levels(test_data[, 'user_country'])=="NULL"] <- "de"

cat("Loading GBM model ...\n")
load("gbM.RData")

y_gbM <- predict(gbM, test_data[, 3:24])
test_data$Y <- y_gbM
op_gbM <- test_data[, c('user_id', 'item_id', 'Y')]

save(op_gbM, file="op_gbM.RData")
write.csv(op_gbM, file="op_gbM.csv", col.names=FALSE, row.names=FALSE)
