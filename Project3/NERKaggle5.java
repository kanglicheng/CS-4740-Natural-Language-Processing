import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.*;
import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.sequences.SeqClassifierFlags;
import edu.stanford.nlp.objectbank.*;
//import edu.stanford.nlp.sequences.DocumentReaderAndWriter;
import edu.stanford.nlp.sequences.*;
import edu.stanford.nlp.util.Triple;

import edu.stanford.nlp.util.StringUtils;
import java.util.Properties;

import java.util.List;
import java.util.ArrayList;

/** This is a java code to use the serialized NER classifier trained by the given data and
 *  to produce the output for Kaggle competition (with the given test data set). The output
 *  is then processed separately with a Matlab code to generate a CSV file with
 *  the following format:
 *  
 *  Type,      Prediction
 *  PER,a-b c-d e-f ...
 *  LOC,a1-b1 c1-d1 ...
 *  ORG,a2-b2 c2-d2 e3-f3 ...
 *  MISC, a3-b3 c3-d3 ...
 *  
 *  Kang-Li S. Cheng
 *  For Project3, CS4740 Introduction to NLP, Cornell University
 *
 * +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 */

/* 
     Usage:

     java NERKaggle5 property-file

 */

public class NERKaggle5 {
    public static void main( String[] args ) throws Exception {
	//the NER property file is loaded from the command-line
	Properties props = StringUtils.propFileToProperties(args[0]);
	// Get the testFile and loadPath from the prop file:

	String testFile = props.getProperty("testFile");
	String loadPath = props.getProperty("loadClassifier");
	//  System.out.println( testFile + '\t'+ loadPath);

	//  Load the NER model by getClassifier: 
	CRFClassifier<CoreLabel> classifier = CRFClassifier.getClassifier(loadPath);

	//  CRFClassifier<CoreLabel> classifier = CRFClassifier.getClassifier(loadPath, props);

	// An instance of the DocumentReaderAndWriter is needed:
	DocumentReaderAndWriter<CoreLabel> readerAndWriter = classifier.makeReaderAndWriter();

	// DocumentReaderAndWriter<CoreLabel> readerAndWriter = classifier.defaultReaderAndWriter();

	// For the Classifier to recognize the input file as a tab separated file: first column  the tokens
	// second column the line numbers, we have to call classifyAndWriteAnswers method:
	// (the third argument prints out the score of the test. It is not relevant for Kaggle test,
	//  but useful in giving the performance scores.)
	//
	// *** Calling any other CRFClassifier methods will result in classifying
	// *** every single token in the test file, which 
	// *** would NOT be  what we want.
	//
	classifier.classifyAndWriteAnswers(testFile, readerAndWriter, false);
    }
      
}
