package com.k2.tikaserver.controller;

import com.k2.tikaserver.TiKaUtils;
import com.k2.tikaserver.exception.BaseException;
import com.k2.tikaserver.model.CustomPair;
import com.k2.tikaserver.model.TextResponse;
import com.k2.tikaserver.service.NLPService;
import com.k2.tikaserver.service.UtilsService;
import org.apache.tika.metadata.Metadata;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayInputStream;
import java.io.InputStream;

@RestController
@RequestMapping("/tika")
public class TikaController
{
    @Autowired
    NLPService nlpService;

    @RequestMapping(method = RequestMethod.POST, value = "/gettext")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file,
                                        @RequestParam(value = "type", required = false, defaultValue = "content") String type,
                                        @RequestParam(value = "raw", required = false, defaultValue = "no") String raw, Model model)
    {
        TextResponse tr = new TextResponse();

        try
        {
            if (file != null)
            {
                String fileName = file.getOriginalFilename();
                InputStream is = new ByteArrayInputStream(file.getBytes());

                {
                    String content = "";
                    Metadata theData = TiKaUtils.extractMetaDataUsingParser(is);
                    StringBuilder sb = new StringBuilder();
                    for (String name : theData.names())
                    {
                        CustomPair pair = new CustomPair(name, theData.get(name));
                        tr.getProperties().add(pair);
                    }
                    is.reset();

                    if (TiKaUtils.IsImageExtension(fileName))
                    {
                        content = TiKaUtils.extractJpgContentUsingOCR(is);
                    }
                    else
                    {
                        content = TiKaUtils.extractContentUsingParser(is);
                    }

                    if (content.trim().length() == 0 && fileName.endsWith("pdf"))
                    {
                        is.reset();
                        content = TiKaUtils.extractPdfContentUsingOCR(is);
                    }

                    if (type.equalsIgnoreCase("concat"))
                    {
                        content = content.replaceAll("(\\r|\\n)", (UtilsService.SPACE));
                        content = content.replaceAll("\\s{2,}", (UtilsService.SPACE)).trim();
                        if (!raw.equalsIgnoreCase("yes")) content = content.replaceAll("/[^A-Za-z0-9 ]/", "");
                    }
                    tr.setResult(content);
                }

                is.close();

                return new ResponseEntity<>(tr, HttpStatus.OK);
            }

            return new ResponseEntity<>(tr, HttpStatus.NO_CONTENT);
        }
        catch (Exception ex)
        {
            throw new BaseException(ex.getMessage(), ex);
        }
    }

    @RequestMapping(method = RequestMethod.POST, value = "/lang")
    public ResponseEntity<?> detectLanguage(@RequestBody String text, Model model)
    {
        return new ResponseEntity<>(nlpService.detectLanguage(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.GET, value = "/stop-words")
    public ResponseEntity<?> stopWords(Model model)
    {
        return new ResponseEntity<>(nlpService.stopWords(), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/sentences-pos")
    public ResponseEntity<?> detectSentencesPos(@RequestBody String text, Model model)
    {
        return new ResponseEntity<>(nlpService.sentencesPos(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/sentences")
    public ResponseEntity<?> detectSentences(@RequestBody String text, Model model)
    {
        return new ResponseEntity<>(nlpService.sentences(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/sentences-value")
    public ResponseEntity<?> detectSentencesValue(@RequestBody String text, Model model)
    {
        return new ResponseEntity<>(nlpService.sentencesValues(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/tokens-pos")
    public ResponseEntity<?> detectPosTokens(@RequestBody String text, Model model)
    {
        return new ResponseEntity<>(nlpService.tokenizePos(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/tokens")
    public ResponseEntity<?> detectTokens(@RequestBody String text, Model model)
    {
        return new ResponseEntity<>(nlpService.tokenize(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/tokens-value")
    public ResponseEntity<?> detectTokenValues(@RequestBody String text, Model model)
    {
        return new ResponseEntity<>(nlpService.tokenizeValues(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/tags")
    public ResponseEntity<?> detectTags(@RequestBody String text, Model model)
    {
        String[] tokens = nlpService.tokenize(text);

        return new ResponseEntity<>(nlpService.tags(tokens), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/lemmas")
    public ResponseEntity<?> detectLemmas(@RequestBody String text, Model model)
    {
        String[] tokens = nlpService.tokenize(text);
        String[] tags = nlpService.tags(tokens);

        return new ResponseEntity<>(nlpService.lemmas(tokens, tags), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/chunks")
    public ResponseEntity<?> detectChunks(@RequestBody String text, Model model)
    {
        String[] tokens = nlpService.tokenize(text);
        String[] tags = nlpService.tags(tokens);

        return new ResponseEntity<>(nlpService.chunks(tokens, tags), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/sanitize")
    public ResponseEntity<?> sanitize(@RequestBody String text, Model model)
    {

        return new ResponseEntity<>(nlpService.sanitize(text), HttpStatus.OK);
    }

    @RequestMapping(method = RequestMethod.POST, value = "/sanitized-text")
    public ResponseEntity<?> sanitizeText(@RequestBody String text, Model model)
    {
        TextResponse tr = new TextResponse();

        tr.setResult(nlpService.toSanitizedString(text));

        return new ResponseEntity<>(tr, HttpStatus.OK);
    }
}
