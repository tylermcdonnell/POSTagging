/* Copyright (C) 2002 Univ. of Massachusetts Amherst, Computer Science Dept.
   This file is part of "MALLET" (MAchine Learning for LanguagE Toolkit).
   http://www.cs.umass.edu/~mccallum/mallet
   This software is provided under the terms of the Common Public License,
   version 1.0, as published by http://www.opensource.org.  For further
   information, see the file `LICENSE' included with this distribution. */




/** 
   @author Andrew McCallum <a href="mailto:mccallum@cs.umass.edu">mccallum@cs.umass.edu</a>
 */

package cc.mallet.fst;


import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;
import java.util.logging.Logger;

import cc.mallet.types.Instance;
import cc.mallet.types.InstanceList;
import cc.mallet.types.Sequence;

import cc.mallet.util.MalletLogger;

/**
 * Evaluates a transducer model based on predictions of individual tokens.
 */
public class TokenAccuracyEvaluator extends TransducerEvaluator
{
	private static Logger logger = MalletLogger.getLogger(TokenAccuracyEvaluator.class.getName());

	private HashMap<String,Double> accuracy = new HashMap<String,Double>();

        private boolean vocabulary_instated = false;
        private HashMap<Object, Integer> vocabulary = new HashMap<Object, Integer>();

	public TokenAccuracyEvaluator (InstanceList[] instanceLists, String[] descriptions) {
		super (instanceLists, descriptions);
	}
	
	public TokenAccuracyEvaluator (InstanceList instanceList1, String description1) {
		this (new InstanceList[] {instanceList1}, new String[] {description1});
	}
	
	public TokenAccuracyEvaluator (InstanceList instanceList1, String description1,
			InstanceList instanceList2, String description2) {
		this (new InstanceList[] {instanceList1, instanceList2}, new String[] {description1, description2});
	}
	
	public TokenAccuracyEvaluator (InstanceList instanceList1, String description1,
			InstanceList instanceList2, String description2,
			InstanceList instanceList3, String description3) {
		this (new InstanceList[] {instanceList1, instanceList2, instanceList3}, new String[] {description1, description2, description3});
	}

	public void evaluateInstanceList (TransducerTrainer trainer, InstanceList instances, String description) 
    {
		int numCorrectTokens;
		int totalTokens;
		
		// New evaluation metric: Out-of-Vocabulary Accuracy.
		int totalOOVTokens;
		int numCorrectOOVTokens;

		// One-Time vocabulary setup.
		if (vocabulary_instated == false)
 		{
		    for (int i = 0; i < instances.size(); i++)
		    {
			Sequence input = (Sequence)instances.get(i).getData();
			for (int j = 0; j < input.size(); j++)
			{       
			    String token = (String)input.get(j).toString();
			    if (!this.vocabulary.containsKey(token))
			    {
				this.vocabulary.put(token, 0);
			    }
			}
		    }
		    vocabulary_instated = true;
		}

		Transducer transducer = trainer.getTransducer();
		totalTokens = numCorrectTokens = totalOOVTokens = numCorrectOOVTokens = 0;
		for (int i = 0; i < instances.size(); i++) {
			Instance instance = instances.get(i);
			Sequence input = (Sequence) instance.getData();
			Sequence trueOutput = (Sequence) instance.getTarget();
			assert (input.size() == trueOutput.size());
			//System.err.println ("TokenAccuracyEvaluator "+i+" length="+input.size());
			Sequence predOutput = transducer.transduce (input);
			assert (predOutput.size() == trueOutput.size());

			for (int j = 0; j < trueOutput.size(); j++) {
			        // Standard Accuracy counts.
				totalTokens++;
				if (trueOutput.get(j).equals(predOutput.get(j)))
					numCorrectTokens++;
				
				// OOV Accuracy counts.
				if (!this.vocabulary.containsKey(input.get(j).toString()))
				{
				    totalOOVTokens += 1;
				    if (trueOutput.get(j).equals(predOutput.get(j)))
					numCorrectOOVTokens += 1;
				}
				
			}
			//System.err.println ("TokenAccuracyEvaluator "+i+" numCorrectTokens="+numCorrectTokens+" totalTokens="+totalTokens+" accuracy="+((double)numCorrectTokens)/totalTokens);
		}
		double acc = ((double)numCorrectTokens)/totalTokens;
		double oovAcc = ((double)numCorrectOOVTokens)/totalOOVTokens;
		//System.err.println ("TokenAccuracyEvaluator accuracy="+acc);
		accuracy.put(description, acc);
		logger.info (description +" accuracy="+acc);
		logger.info (description +" OOV accuracy="+oovAcc);
	}

	/**
	 * Returns the accuracy from the last time test() or evaluate() was called
	 * @return
	 */
	public double getAccuracy (String description)
	{
		Double ret = accuracy.get(description);
		if (ret != null)
			return ret.doubleValue();
		throw new IllegalArgumentException ("No accuracy available for instance list \""+description+"\"");
	}
}
