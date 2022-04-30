package com.k2.tikaserver;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

/**
 * Main application class
 */
@SpringBootApplication
@EnableConfigurationProperties({NLPProperties.class})
public class TikaServerApp
{
    private static final Logger LOG = LoggerFactory.getLogger(TikaServerApp.class);

    public static void main(String[] args)
    {
        SpringApplication.run(TikaServerApp.class, args);
    }
}
