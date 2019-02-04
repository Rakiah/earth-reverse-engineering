#!/bin/bash

INPUT_PATH=$1
OUTPUT_PATH=$2

case "$(uname -s)" in

   Darwin)
     echo 'This script doesnt support MacOS platform'
     ;;

   Linux)
     echo 'This script doesnt support Linux platform'
     ;;

   CYGWIN*|MINGW32*|MINGW64*|MSYS*)
     ./draco/windows/draco_encoder -i $INPUT_PATH -o $OUTPUT_PATH
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
     echo 'This script doesnt recognize and support your platform' 
     ;;
esac

echo "Draco encoding script finished !"
