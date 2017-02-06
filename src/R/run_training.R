source('header.R')

cat("Reading training data ...\n")
load("train_data_final_ordered.rdata")

gbmGrid <- expand.grid(interaction.depth = c(7),
                       n.trees = 500,
                       shrinkage = c(.1),
                       n.minobsinnode = c(10))

cat("Training GBM ... ")

gbM <- train(Y~., data=train_data, preProc=c("center","scale"),
	method="gbm", tuneGrid = gbmGrid, trControl=trainControl(method="repeatedcv", number=3, repeats=1)
	)
save(gbM, file="gbM.RData")
