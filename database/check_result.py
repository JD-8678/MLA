import csv

def main():
    with open('result.csv','w') as res:
        with open('news-querie.tsv') as news_file:
            with open('vclaims.tsv') as vclaims_file:
                with open('/home/erwin/Programming/Python/clef2020-factchecking-task2/result.tsv') as result_file:
                    writer = csv.writer(res,delimiter=',')
                    reader_news = csv.reader(news_file, delimiter='\t')
                    reader_vclaims = csv.reader(vclaims_file, delimiter='\t')
                    reader_result = csv.reader(result_file, delimiter='\t')

                    count = -1
                    current = -1
                    for row in reader_result:
                        if count >= 0:
                            #print(row)

                            vclaims_file.seek(0)

                            vclaims_content = ""
                            score = row[4]
                            for claims in reader_vclaims:
                                if(claims[0] == row[2]):
                                    vclaims_content = claims[1]
                                    break
                            #print([row[0],vclaims_content,score])
                            writer.writerow([row[0],vclaims_content,score])
                            count -= 1
                            current = row[0]
                        else:
                            if current != row[0]:
                                count = 10
                                #print(row)

                                vclaims_file.seek(0)
                                news_file.seek(0)

                                news_content = ""
                                for news in reader_news:
                                    if(news[0] == row[0]):
                                        news_content = news[1]
                                        break
                                #print(news_content)
                                writer.writerow([news_content,'',0])

                                vclaims_content = ""
                                score = row[4]
                                for claims in reader_vclaims:
                                    if(claims[0] == row[2]):
                                        vclaims_content = claims[1]
                                        break
                                #print([row[0],vclaims_content,score])
                                writer.writerow([row[0],vclaims_content,score])
                            


if __name__ == "__main__":
    main()