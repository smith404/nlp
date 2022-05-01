/*
 * Copyright (c) 2022. All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

package com.k2.tikaserver.service.impl;

import com.k2.tikaserver.NLPProperties;
import com.k2.tikaserver.model.Prediction;
import com.k2.tikaserver.model.Token;
import com.k2.tikaserver.service.NLPService;
import com.k2.tikaserver.service.UtilsService;
import opennlp.tools.chunker.ChunkerME;
import opennlp.tools.chunker.ChunkerModel;
import opennlp.tools.langdetect.Language;
import opennlp.tools.langdetect.LanguageDetector;
import opennlp.tools.langdetect.LanguageDetectorME;
import opennlp.tools.langdetect.LanguageDetectorModel;
import opennlp.tools.lemmatizer.DictionaryLemmatizer;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.util.Span;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Service("NLPService")
public class NLPServiceImpl implements NLPService
{
    private static final Logger log = LoggerFactory.getLogger(NLPServiceImpl.class);
    private static final String CLAUSE_SPLIT_REGEX = "\\r\\n|\\n|\\r";

    @Autowired
    private NLPProperties nlpProperties;

    // Open NLP variables
    private LanguageDetector ld;
    private TokenizerME tokenizer;
    private POSTaggerME tagger;
    private SentenceDetectorME sentenceDetector;
    private ChunkerME chunker;
    private DictionaryLemmatizer lemmatizer;
    private List<String> stopWords;

    @PostConstruct
    public void init()
    {
        // Standard NLP Models
        initTokenizer();
        initTagger();
        initSentenceDetector();
        initLemmatizer();
        initChunker();
        initStopWords();

        // Language detection model
        initLanguageDetection();
    }

    public void initTokenizer()
    {
        try
        {
            Path location = Paths.get(nlpProperties.getNlpRootLocation());
            File modelFile = new File(location + "/" + nlpProperties.getTokenizerModel());
            InputStream dataIn = new FileInputStream(modelFile);

            TokenizerModel tokenModel = new TokenizerModel(dataIn);
            tokenizer = new TokenizerME(tokenModel);
            log.info("NLP ** Loaded token model, using model file: {}", nlpProperties.getTokenizerModel());
        }
        catch (Exception ex)
        {
            log.warn(UtilsService.makeExceptionWarning(ex), "NLP");
        }
    }

    public void initStopWords()
    {
        try
        {
            String path = nlpProperties.getNlpRootLocation() + "/" + nlpProperties.getStopWords();

            try (Stream<String> lines = Files.lines(Paths.get(path)))
            {
                stopWords = lines.collect(Collectors.toList());
            }
            log.info("NLP ** Loaded stop words, using model file: {}", nlpProperties.getStopWords());
        }
        catch (Exception ex)
        {
            log.warn(UtilsService.makeExceptionWarning(ex), "NLP");
        }
    }

    public void initTagger()
    {
        try
        {
            Path location = Paths.get(nlpProperties.getNlpRootLocation());
            File modelFile = new File(location + "/" + nlpProperties.getTaggerModel());
            InputStream dataIn = new FileInputStream(modelFile);

            POSModel taggerModel = new POSModel(dataIn);
            tagger = new POSTaggerME(taggerModel);
            log.info("NLP ** Loaded tagger model, using model file: {}", nlpProperties.getTaggerModel());
        }
        catch (Exception ex)
        {
            log.warn(UtilsService.makeExceptionWarning(ex), "NLP");
        }
    }

    public void initSentenceDetector()
    {
        try
        {
            Path location = Paths.get(nlpProperties.getNlpRootLocation());
            File modelFile = new File(location + "/" + nlpProperties.getSentModel());
            InputStream dataIn = new FileInputStream(modelFile);

            SentenceModel sentenceModel = new SentenceModel(dataIn);
            sentenceDetector = new SentenceDetectorME(sentenceModel);
            log.info("NLP ** Loaded sentence model, using model file: {}", nlpProperties.getSentModel());
        }
        catch (Exception ex)
        {
            log.warn(UtilsService.makeExceptionWarning(ex), "NLP");
        }
    }

    public void initLemmatizer()
    {
        try
        {
            Path location = Paths.get(nlpProperties.getNlpRootLocation());
            File modelFile = new File(location + "/" + nlpProperties.getLemmatizerDict());
            InputStream dataIn = new FileInputStream(modelFile);

            lemmatizer = new DictionaryLemmatizer(dataIn);
            log.info("NLP ** Loaded lemmatizer dictionary, using file: {}", nlpProperties.getLemmatizerDict());
        }
        catch (Exception ex)
        {
            log.warn(UtilsService.makeExceptionWarning(ex), "NLP");
        }
    }

    public void initChunker()
    {
        try
        {
            Path location = Paths.get(nlpProperties.getNlpRootLocation());
            File modelFile = new File(location + "/" + nlpProperties.getChunkerModel());
            InputStream dataIn = new FileInputStream(modelFile);

            ChunkerModel chunkerModel = new ChunkerModel(dataIn);
            chunker = new ChunkerME(chunkerModel);
            log.info("NLP ** Loaded chunker model, using model file: {}", nlpProperties.getChunkerModel());
        }
        catch (Exception ex)
        {
            log.warn(UtilsService.makeExceptionWarning(ex), "NLP");
        }
    }

    public void initLanguageDetection()
    {
        try
        {
            Path location = Paths.get(nlpProperties.getNlpRootLocation());
            File modelFile = new File(location + "/" + nlpProperties.getLanguageModel());
            InputStream dataIn = new FileInputStream(modelFile);

            LanguageDetectorModel languageModel = new LanguageDetectorModel(dataIn);
            ld = new LanguageDetectorME(languageModel);
            log.info("NLP ** Loaded language model, using model file: {}", nlpProperties.getLanguageModel());
        }
        catch (Exception ex)
        {
            log.warn(UtilsService.makeExceptionWarning(ex), "NLP");
        }

    }

    @Override
    public Prediction detectLanguage(String text)
    {
        Prediction pr = new Prediction();
        pr.setCategory("eng");

        if (ld == null) return pr;

        Language[] languages = ld.predictLanguages(text);

        double score = -1;
        for (Language lg : languages)
        {
            if (lg.getConfidence() > score)
            {
                score = lg.getConfidence();
                pr.setCategory(lg.getLang());
                pr.setProbability(lg.getConfidence());
            }
        }

        return pr;
    }

    @Override
    public List<String> stopWords()
    {
        return stopWords;
    }

    @Override
    public String[] sentences(String text)
    {
        return sentenceDetector.sentDetect(text);
    }

    @Override
    public Span[] sentencesPos(String text)
    {
        return sentenceDetector.sentPosDetect(text);
    }

    @Override
    public Token[] sentencesValues(String text)
    {
        Span[] spans = sentenceDetector.sentPosDetect(text);
        String[] values = sentenceDetector.sentDetect(text);

        if (spans.length != values.length)
        {
            log.warn("Error creating token array");
            return new Token[0];
        }

        Token[] tokens = new Token[spans.length];
        for (int i = 0; i < spans.length; ++i)
        {
            Token t = new Token(spans[i], values[i], "SENT");
            tokens[i] = t;
        }

        return tokens;
    }

    @Override
    public String[] tokenize(String text)
    {
        return tokenizer.tokenize(text);
    }

    @Override
    public Span[] tokenizePos(String text)
    {
        return tokenizer.tokenizePos(text);
    }

    @Override
    public Token[] tokenizeValues(String text)
    {
        Span[] spans = tokenizer.tokenizePos(text);
        String[] values = tokenizer.tokenize(text);
        String[] tags = tagger.tag(values);
        String[] lemmas = lemmas(values, tags);

        if (spans.length != values.length)
        {
            log.warn("Error creating token array");
            return new Token[0];
        }

        Token[] tokens = new Token[spans.length];
        for (int i = 0; i < spans.length; ++i)
        {
            String lemma = lemmas[i].equalsIgnoreCase("O") ? values[i].toLowerCase(Locale.ROOT) : lemmas[i];
            Token t = new Token(spans[i], values[i], lemma.toLowerCase(Locale.ROOT), tags[i]);
            tokens[i] = t;
        }

        return tokens;
    }

    @Override
    public String[] tags(String[] tokens)
    {
        return tagger.tag(tokens);
    }

    @Override
    public String[] lemmas(String[] tokens, String[] tags)
    {
        return lemmatizer.lemmatize(tokens, tags);
    }

    @Override
    public String[] chunks(String[] tokens, String[] tags)
    {
        return chunker.chunk(tokens, tags);
    }

    @Override
    public List<Token> splitClauses(String text)
    {
        List<Token> clauses = new ArrayList<>();

        Token[] sentences = sentencesValues(sanitizeLines(text));
        Token lastSentence = null;
        for (Token sentence : sentences)
        {
            if (lastSentence == null)
            {
                lastSentence = sentence;
                lastSentence.setType("PARA");
                continue;
            }

            if (sentence.getStart() == lastSentence.getEnd() + UtilsService.NEWLINE.length())
            {
                // Merge the sentences
                lastSentence.setValue(lastSentence.getValue() + " " + sentence.getValue());
                lastSentence.setLength(lastSentence.getLength() + sentence.getLength() + UtilsService.NEWLINE.length());
            }
            else
            {
                clauses.add(lastSentence);
                lastSentence = sentence;
                lastSentence.setType("PARA");
            }
        }

        // Add the last entry
        clauses.add(lastSentence);
        lastSentence.setType("PARA");

        return clauses;
    }

    @Override
    public List<Token> sanitize(String text)
    {
        Token[] tokens = tokenizeValues(UtilsService.cleanWhiteSpace(UtilsService.makeAlphaNumeric(text, true)));

        return Arrays.stream(tokens).filter(
                c -> !(stopWords.contains(c.getLemma()))
        ).collect(Collectors.toList());
    }

    @Override
    public String toSanitizedString(String text)
    {
        List<Token> results = sanitize(text);

        StringBuilder sb = new StringBuilder();
        for (Token entity : results)
        {
            sb.append(entity.getLemma());
            sb.append(" ");
        }

        return sb.toString().trim();
    }

    public String sanitizeLines(String text)
    {
        StringBuilder sb = new StringBuilder();

        Stream<String> lines = text.lines();

        lines.forEach(line -> {
            sb.append(Normalizer.normalize(line, Normalizer.Form.NFD).trim()
                    .replaceAll(" +", " ")
                    .replaceAll("[^A-Za-z0-9-.,:; ]", ""));
            sb.append(UtilsService.NEWLINE);
        });

        return sb.toString();
    }
}