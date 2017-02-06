source('header.R')

cat("Reading training description ...\n")
train_data = read.table("training/trainingXforR.csv", sep = ",", header=FALSE)

cat("Reading training labels ...\n")
y = as.integer(scan(file="training/trainingYforR.csv", what="integer", sep=","))

train_data$Y <- y

features <- c('previous_interaction', 
			  'user_career_level', 
			  'user_discipline_id',
			  'user_industry_id',
			  'user_country',
			  'user_region',
			  'user_experience_entries',
			  'user_experience_years',
			  'user_experience_current',
			  'user_education_degree',
			  'item_career_level',
			  'item_discipline_id',
			  'item_industry_id',
			  'item_region',
			  'item_country',
			  'match_num_jobroles',
			  'match_num_tags',
			  'match_career_level',
			  'match_discipline_id',
			  'match_industry_id',
			  'match_region',
			  'match_country',
			  'interaction_type'
			  )

colnames(train_data) <- features

train_data$previous_interaction <- ifelse(train_data$previous_interaction==4, -1, train_data$previous_interaction)

no_factor <- c('previous_interaction',
	           'user_country',
	           'match_num_jobroles',
			   'match_num_tags',
			   'interaction_type'
     		  )

to_order <- c('user_career_level',
			  'user_experience_entries',
			  'user_experience_years',
			  'user_experience_current',
			  'user_education_degree',
			  'item_career_level'
			 )

to_impute <- c('user_region',
               'user_experience_entries',
               'user_experience_years',
               'user_experience_current',
               'user_education_degree',
               'item_career_level'
              )

for(feature in features){
    if(feature %in% no_factor) next;
    if(feature %in% to_order){
        if(feature %in% to_impute)
            test_data[, feature] <- factor(ifelse(is.na(test_data[, feature]), 
                                                  median(test_data[, feature], na.rm = TRUE), 
                                                  test_data[, feature]
                                                  ), 
                                            ordered=TRUE
                                            )
        else
            test_data[, feature] <- factor(test_data[, feature], ordered=TRUE)
    }
    else{
        if(feature %in% to_impute)
            test_data[, feature] <- factor(ifelse(is.na(test_data[, feature]),
                                                  median(test_data[, feature], na.rm = TRUE), 
                                                  test_data[, feature]
                                                  )
                                            )
        else
            test_data[, feature] <- factor(test_data[, feature])
    }
}


summary(train_data)
save(train_data, file="train_data_final_ordered.rdata")
