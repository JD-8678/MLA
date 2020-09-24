import flask,csv,json
import os
import bin

app = flask.Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    reader=[["elem_0","elem_1","elem_2","elem_3","elem_4"],
                ["elem_0","elem_1","elem_2","elem_3","elem_4"],
                ["elem_0","elem_1","elem_2","elem_3","elem_4"],
                ["elem_0","elem_1","elem_2","elem_3","elem_4"],
                ["elem_0","elem_1","elem_2","elem_3","elem_4"]]
                
    test={
                "mode": "url",
                "url": "https://www.bbc.com/news/world-us-canada-54171941",
                "index_name": "vclaims",
                "fulltext": "John Bolton: Criminal inquiry opened into explosive memoir\nPresident Donald Trump's former National Security Adviser John Bolton is being investigated for possibly disclosing classified information when he published his memoir in June.\nThe US Department of Justice launched a criminal case after failing to stop the publication of The Room Where It Happened book.\nMr Bolton denies all the accusations.\nIn the book, Mr Trump is depicted as a president ignorant of geopolitical facts.\nMr Bolton, who served as MrTrump's national security adviser in 2018-19, also alleges the president's decisions are driven by a desire for re-election\nAt the time of publication, President Trump made it clear that he wanted his former aide prosecuted, describing him as \"grossly incompetent\" and \"a liar\".\nThe case would focus on Mr Bolton's claim that his manuscript had passed through a pre-publication national security review, and claims by critics that it did not complete that review.\nA grand jury convened by the Department of Justice has now formally issued subpoenas to the Simon & Schuster publishing company and the Javelin Agency, which represents Mr Bolton.\nIn a statement, Mr Bolton's lawyer Charles J. Cooper said: \"Ambassador Bolton emphatically rejects any claim that he acted improperly, let alone criminally, in connection with the publication of his book, and he will cooperate fully, as he has throughout, with any official inquiry into his conduct.\"\nWhat does the book say about President Trump?\nMany of Mr Bolton's allegations are based on private conversations and are impossible to verify.\nAmong them are the following claims:\n- President Trump sought help from Chinese President Xi Jinping to win the 2020 vote, stressing the \"importance of farmers and increased Chinese purchases of soybeans and wheat in the electoral outcome\"\n- He also said China's construction of internment camps in the Xinjiang region was the \"right thing to do\"\n- President Trump was willing to intervene in criminal investigations \"to, in effect, give personal favours to dictators he liked\". Mr Bolton said Mr Trump was willing to assist Turkish President Recep Tayyip Erdogan over a case involving a Turkish company\n- The US leader said invading Venezuela would be \"cool\" and that the South American nation was \"really part of the United States\"\n- Mr Trump was unaware the UK was a nuclear power and once asked a senior aide if Finland was part of Russia\nJust days before the book's publication, President Trump said the book was \"made up of lies and fake stories\".\n\"Many of the ridiculous statements he attributes to me were never made, pure fiction. Just trying to get even for firing him like the sick puppy he is!\" Mr Trump said in a tweet.",
                "split": [
                    {
                        "sentence": "John Bolton: Criminal inquiry opened into explosive memoir",
                        "retrieved": {
                            "1": {
                                "_id": "6415",
                                "combined_score": 1.0,
                                "_score": 16.733406,
                                "cosine": 1.679291769285,
                                "vclaim": "Says John Bolton 'fundamentally was a man of the left.'",
                                "link": "http://www.politifact.com/punditfact/statements/2019/sep/13/tucker-carlson/tucker-carlson-falsely-claims-john-bolton-was-man-/"
                            },
                            "2": {
                                "_id": "4642",
                                "combined_score": 0.774191658928,
                                "_score": 12.494736,
                                "cosine": 1.582796470095,
                                "vclaim": "Says John Bolton supported the Iraq War and said last year that 'I still think the decision to overthrow Saddam was correct.'",
                                "link": "http://www.politifact.com/truth-o-meter/statements/2016/nov/17/rand-paul/rand-paul-says-john-bolton-still-thinks-iraq-war-w/"
                            },
                            "3": {
                                "_id": "26006",
                                "combined_score": 0.649661271827,
                                "_score": 15.171744,
                                "cosine": 1.424580558367,
                                "vclaim": "The FBI announced an inquiry into Russian ties between the Trump campaign and the Russian government.",
                                "link": "https://www.snopes.com/fact-check/manafort-ties-to-russia/"
                            },
                            "4": {
                                "_id": "4510",
                                "combined_score": 0.632137455716,
                                "_score": 7.4315767,
                                "cosine": 1.572275295008,
                                "vclaim": "Says his conviction is 'a political witch hunt by holdovers in the Obama justice department.'",
                                "link": "http://www.politifact.com/truth-o-meter/statements/2017/aug/29/joe-arpaio/arpaio-falsely-ties-conviction-obama-administratio/"
                            },
                            "5": {
                                "_id": "26181",
                                "combined_score": 0.615316437949,
                                "_score": 8.431206,
                                "cosine": 1.537544493883,
                                "vclaim": "A half dozen Trump-related entities were under criminal investigation in December 2018.",
                                "link": "https://www.snopes.com/fact-check/trump-entities-criminal-probe/"
                            }
                        }
                    },
                    {
                        "sentence": "President Donald Trump's former National Security Adviser John Bolton is being investigated for possibly disclosing classified information when he published his memoir in June.",
                        "retrieved": {
                            "1": {
                                "_id": "6163",
                                "combined_score": 0.819450030703,
                                "_score": 24.131187,
                                "cosine": 1.618312459957,
                                "vclaim": "'The FBI said (former national security adviser Michael Flynn) wasn't lying.'",
                                "link": "http://www.politifact.com/truth-o-meter/statements/2019/mar/28/donald-trump/no-fbi-did-not-say-michael-flynn-did-not-lie-donal/"
                            },
                            "2": {
                                "_id": "6415",
                                "combined_score": 0.814228342704,
                                "_score": 16.733406,
                                "cosine": 1.699669421781,
                                "vclaim": "Says John Bolton 'fundamentally was a man of the left.'",
                                "link": "http://www.politifact.com/punditfact/statements/2019/sep/13/tucker-carlson/tucker-carlson-falsely-claims-john-bolton-was-man-/"
                            },
                            "3": {
                                "_id": "7671",
                                "combined_score": 0.813793825566,
                                "_score": 20.471539,
                                "cosine": 1.656479962997,
                                "vclaim": "Says former FBI Director James Comey admitted to leaking classified information.",
                                "link": "http://www.politifact.com/north-carolina/statements/2017/jun/09/north-carolina-republican-party/james-comey-hearings-did-former-fbi-director-admit/"
                            },
                            "4": {
                                "_id": "32282",
                                "combined_score": 0.793714415409,
                                "_score": 21.117102,
                                "cosine": 1.635485181892,
                                "vclaim": "President Trump's son Barron won a national academic award in June 2017.",
                                "link": "https://www.snopes.com/fact-check/barron-trump-wins-national-academic-award/"
                            },
                            "5": {
                                "_id": "26990",
                                "combined_score": 0.787428642377,
                                "_score": 24.692327,
                                "cosine": 1.590205812217,
                                "vclaim": "Republican presidential candidate Donald Trump leaked classified information about a U.S. military base in Saudi Arabia after receiving his first national security intelligence briefing.",
                                "link": "https://www.snopes.com/fact-check/trump-leaks-classified-info/"
                            }
                        }
                    }
                ]
            }
        
    maintext = ["This is the maintext.","and this is the secend sentence"]
    if flask.request.method == 'POST':
        task_content = flask.request.form['content']
        print(task_content)

        result = bin.run_url.run(task_content)
        #print(result.values)

        #reader=result.values

        return flask.render_template('/main.html', claims=[[]], text=maintext, textClaims=test)
    else:
        return flask.render_template('/main.html', claims=[[]], text=maintext, textClaims=test)

#def parse_args(mode,input):
#    parser = argparse.ArgumentParser()
#    parser.add_argument("--predict-file", "-p", default="result.csv",
#                        help="File in TREC Run format containing the model predictions")
#    parser.add_argument("--keys", "-k",nargs='+', default=['vclaim', 'title', 'named_entities_claim', 'named_entities_article','keywords'],
#                        help="Keys to search in the document")
#    parser.add_argument("--size", "-s", default=10000,
#                        help="Maximum results extracted for a query")
#    parser.add_argument("--output_size", "-x", default=10000,
#                        help="Maximum results extracted for news")
#    parser.add_argument("--conn", "-c", default="127.0.0.1:9200",
#                        help="HTTP/S URI to a instance of ElasticSearch")
#    parser.add_argument("--mode", "-m", default="url", choices=["url","string"], type=str.lower,
#                        help="choice between url or string mode")
#    parser.add_argument("--input", "-i", nargs='+', required=True,
#                        help="input should be a String or url")
#    return parser.parse_args(['--mode',mode,'--input',input])

if __name__ == "__main__":
        app.run(debug=True)