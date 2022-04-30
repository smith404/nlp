/*
 * Copyright (c) 2022. All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

package com.k2.tikaserver;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "nlp")
public class NLPProperties
{
    private boolean trainingSystem = false;

    // Data directories
    private String nlpRootLocation = "nlp-data-root";

    // Default models
    private String tokenizerModel = "eng-token.bin";
    private String taggerModel = "eng-pos-maxent.bin";
    private String sentModel = "eng-sent.bin";
    private String lemmatizerModel = "eng-lemmatizer.bin";
    private String lemmatizerDict = "eng-lemmatizer.dict";
    private String chunkerModel = "eng-chunker.bin";
    private String languageModel = "lang-detect.bin";
    private String stopWords = "eng-stopwords.txt";

    private String defaultLanguage = "eng";

    public String getNlpRootLocation()
    {
        return nlpRootLocation;
    }

    public void setNlpRootLocation(String nlpRootLocation)
    {
        this.nlpRootLocation = nlpRootLocation;
    }

    public String getTokenizerModel()
    {
        return tokenizerModel;
    }

    public void setTokenizerModel(String tokenizerModel)
    {
        this.tokenizerModel = tokenizerModel;
    }

    public String getLanguageModel()
    {
        return languageModel;
    }

    public void setLanguageModel(String languageModel)
    {
        this.languageModel = languageModel;
    }

    public boolean isTrainingSystem()
    {
        return trainingSystem;
    }

    public void setTrainingSystem(boolean trainSystem)
    {
        this.trainingSystem = trainSystem;
    }

    public String getTaggerModel()
    {
        return taggerModel;
    }

    public void setTaggerModel(String taggerModel)
    {
        this.taggerModel = taggerModel;
    }

    public String getSentModel()
    {
        return sentModel;
    }

    public void setSentModel(String sentModel)
    {
        this.sentModel = sentModel;
    }

    public String getLemmatizerModel()
    {
        return lemmatizerModel;
    }

    public void setLemmatizerModel(String lemmatizerModel)
    {
        this.lemmatizerModel = lemmatizerModel;
    }

    public String getLemmatizerDict()
    {
        return lemmatizerDict;
    }

    public void setLemmatizerDict(String lemmatizerDict)
    {
        this.lemmatizerDict = lemmatizerDict;
    }

    public String getChunkerModel()
    {
        return chunkerModel;
    }

    public void setChunkerModel(String chunkerModel)
    {
        this.chunkerModel = chunkerModel;
    }

    public String getDefaultLanguage()
    {
        return defaultLanguage;
    }

    public void setDefaultLanguage(String defaultLanguage)
    {
        this.defaultLanguage = defaultLanguage;
    }

    public String getStopWords()
    {
        return stopWords;
    }

    public void setStopWords(String stopWords)
    {
        this.stopWords = stopWords;
    }
}

