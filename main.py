import cv2
import numpy as np
import os
import Plates
import Chars
import KNNFile
showOperation = False

def main():
    KNNData = KNNFile.loadKNNData() #Running training of KNN

    if KNNData!=True:
        print "\n UNABLE TO RUN KNN TRAINING \n"
        return

    originalimage  = cv2.imread("(5).jpg")

    if originalimage is None:
        print "\n UNABLE TO READ IMAGE PROPERLY, PLEASE TRY AGAIN  "
        return

    listOfPossiblePlates = Plates.getPossiblePlates(originalimage)

    #now we move towards obtaining proper characters in the plates by using various constraints
    #we are only sending the list of possible plates obtained in the previous function call
    listOfPossibleCharsInPossiblePlates = Chars.getPossibleCharsInPlates(listOfPossiblePlates)

    cv2.imshow("Original Image", originalimage)            # show scene image

    if len(listOfPossiblePlates) == 0:                          # if no plates were found
        print "\nno license plates were detected\n"             # inform user no plates were found
    else:                                                       # else

        #We have to now find the plates with the most number of recognized characters.
        #Hence we sort in descending order and take the plate with most characters
        listOfPossibleCharsInPossiblePlates.sort(key = lambda possibleCharsinPlate: len(possibleCharsinPlate.strChars), reverse = True)


        finalPlate = listOfPossibleCharsInPossiblePlates[0]

        cv2.imshow("imgPlate", finalPlate.imgPlate)           # show crop of plate and threshold of plate
        cv2.imshow("imgThresh", finalPlate.imgThresh)
        cv2.waitKey()
        if len(finalPlate.strChars) == 0:                     # if no chars were found in the plate
            print "\nNo characters were detected\n\n"       # show message
            return

        drawBoxAroundPlate(originalimage, finalPlate)
        # draw red rectangle around plate
        print "----------------------------------------"
        print "\nThe registration number is: = " + finalPlate.strChars + "\n"       # write license plate text to std out
        print "----------------------------------------"

        cv2.imshow("Final Image", originalimage)
        cv2.waitKey()

        return


####################################################################3

def drawBoxAroundPlate(originalImage,finalPlate):

    getCoordinates = cv2.boxPoints(finalPlate.rrLocationOfPlateInScene)
    RED=(0,0,255.0)
    cv2.line(originalImage, tuple(getCoordinates[0]), tuple(getCoordinates[1]),RED, 2)
    cv2.line(originalImage, tuple(getCoordinates[1]), tuple(getCoordinates[2]),RED, 2)
    cv2.line(originalImage, tuple(getCoordinates[2]), tuple(getCoordinates[3]),RED, 2)
    cv2.line(originalImage, tuple(getCoordinates[3]), tuple(getCoordinates[0]),RED, 2)

###########################################################################


if __name__ == "__main__":
    main()


