package com.example.app;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.Statement;

public class UnsafeQueryService {

    public String buildUserQuery(String userInput) {
        // Intentionally vulnerable: SQL injection pattern
        return "SELECT * FROM users WHERE username = '" + userInput + "'";
    }

    public void runUnsafeQuery(Connection connection, String userInput) throws Exception {
        String query = "SELECT * FROM users WHERE username = '" + userInput + "'";
        Statement stmt = connection.createStatement();
        stmt.execute(query);
    }

    public void runSystemCommand(String host) throws IOException {
        // Intentionally vulnerable: command injection pattern
        Runtime.getRuntime().exec("ping -c 1 " + host);
    }

    public Object unsafeDeserialize(String json) throws Exception {
        // Intentionally unsafe pattern for demo purposes
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(json, Object.class);
    }

    public String weakHash(String value) throws Exception {
        // Intentionally weak crypto
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] digest = md.digest(value.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
