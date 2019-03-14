#!/bin/bash

if [ -z "$1" ]; then
   echo "Convert web page of URL into a pdf file. Requires curl and jq."
   echo
   echo "USAGE:"
   echo "    webpdf.sh URL"
   echo
   echo "EXAMPLE:"
   echo "    webpdf.sh https://www.google.com"
   exit 1
fi

URL=$1
TMP_FILE='/tmp/__web___'
TOKEN=$(curl -s -X POST -H 'Content-Length: 0' https://www.web2pdfconvert.com/token/create)
echo 'TOKEN:' $TOKEN

curl -s -X POST  -F  "url=$URL" "https://www.web2pdfconvert.com/api/web/to/pdf?apikey=776622705&token=${TOKEN}&storefile=true&filename=pdf_web" > ${TMP_FILE}
PDF_URL=$(jq -r '.Files[0].Url' ${TMP_FILE})
echo 'PDF URL:', $PDF_URL

if [[ $PDF_URL == http* ]]; then
   curl ${PDF_URL} --output pdf_web.pdf
fi

