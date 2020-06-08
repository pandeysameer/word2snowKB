###############################

import pysnow

import csv

 

c = pysnow.Client(user="tony.stark ", password="&I@mIronMan", instance="dev19996")

AH_articles = c.resource(api_path='/table/kb_template_kcs_article')

 

count = 0

reader = csv.DictReader(open("data.csv"))

for row in reader:

    print(row['OldName']," to ->"+row['NewName'])

    qb = (

        pysnow.QueryBuilder()

            .field('u_km_id').equals('AH')

            .AND()

            .field('kb_resolution').contains(row['OldName'])

    )

    response = AH_articles.get(query=qb)

    for record in response.all():

        #print the sysID of the KB record

        print(record['sys_id'])

        #kb_resolution is where Old resolver groups are mentioned.

        resolution_text= record['kb_resolution']

        newResolution_text = resolution_text.replace(row['OldName'], row['NewName'])

        newQb = (

            pysnow.QueryBuilder()

                .field("sys_id").equals(record['sys_id'])

        )

        update = {'kb_resolution': newResolution_text}

        updated_record = AH_articles.update(query={'sys_id': record['sys_id']}, payload=update)

        #print the response and HTTP code

        print(updated_record)

        print("Modified the article with the number: "+record['number'])

 

################################