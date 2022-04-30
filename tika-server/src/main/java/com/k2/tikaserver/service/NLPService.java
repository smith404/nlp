package com.k2.tikaserver.service;

import com.k2.tikaserver.model.Clause;
import com.k2.tikaserver.model.Prediction;
import com.k2.tikaserver.model.Token;
import opennlp.tools.util.Span;

import java.util.List;

public interface NLPService
{
    List<String> stopWords();

    String[] sentences(String text);

    Span[] sentencesPos(String text);

    String[] tokenize(String text);

    Span[] tokenizePos(String text);

    String[] tags(String[] tokens);

    String[] lemmas(String[] tokens, String[] tags);

    String[] chunks(String[] tokens, String[] tags);

    List<Clause> splitClauses(String text);

    Prediction detectLanguage(String text);

    Token[] sentencesValues(String text);

    Token[] tokenizeValues(String text);

    List<Token> sanitize(String text);

    String toSanitizedString(String text);
}
