from ES_Database import ElasticsearchStorage
import csv, json

def main():
    with open('./backup/news.csv') as news:     
        reader = csv.DictReader(news, delimiter=',')
        with open('news-querie.tsv','w') as querie:
            writer = csv.writer(querie, delimiter='\t')
            line = 0
            writer.writerow(["","tweet_content"])
            for row in reader:
                if row['maintext'] != None and row['maintext'] != "":
                    writer.writerow([line,row['maintext'].replace('\t','\b')])
                    line += 1

    with open('./backup/claims.csv') as news:     
        reader = csv.DictReader(news, delimiter=',')
        with open('vclaims.tsv','w') as querie:
            writer = csv.writer(querie, delimiter='\t')
            line = 0
            writer.writerow(["","vclaim","title"])
            for row in reader:
                if row['claimReview_claimReviewed'] != None:
                    if row['extra_title'] == None:
                        writer.writerow([line,row['claimReview_claimReviewed'].replace('\t','\b'),row['claimReview_claimReviewed'].replace('\t','\b')])
                    else:
                        writer.writerow([line,row['claimReview_claimReviewed'].replace('\t','\b'),row['extra_title'].replace('\t','\b')])
                    line += 1


if __name__ == "__main__":
    main()