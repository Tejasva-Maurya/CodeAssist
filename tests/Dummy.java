package com.example;

import java.util.List;
import java.util.ArrayList;

/**
 * This is a dummy class for testing the extractor.
 */
public class DummyService {

    // A simple field
    private String name;

    /**
     * Constructor for DummyService
     */
    public DummyService(String name) {
        this.name = name;
    }

    /*
     * This method fetches data and calls another method.
     */
    public void fetchData() {
        System.out.println("Fetching data for " + name);
        processData();
    }

    private void processData() {
        List<String> items = new ArrayList<>();
        items.add("Item 1");
        // Loop through items
        for (String item : items) {
            System.out.println(item);
        }
    }
}
