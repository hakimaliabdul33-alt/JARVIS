package com.jarvis.assistant;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.content.SharedPreferences;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.*;
import android.graphics.Color;
import android.view.Gravity;
import org.json.JSONArray;
import org.json.JSONObject;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.*;
import java.util.Locale;

public class MainActivity extends Activity {

    LinearLayout layout, messages;
    EditText apiKey, question;
    TextView status;
    TextToSpeech tts;
    SharedPreferences prefs;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        prefs = getSharedPreferences("jarvis_settings", MODE_PRIVATE);

        tts = new TextToSpeech(this, result -> {
            if (result == TextToSpeech.SUCCESS) {
                tts.setLanguage(new Locale("hi", "IN"));
            }
        });

        ScrollView scroll = new ScrollView(this);
        layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(20, 20, 20, 20);
        layout.setBackgroundColor(Color.rgb(12, 18, 32));
        scroll.addView(layout);
        setContentView(scroll);

        TextView title = new TextView(this);
        title.setText("J.A.R.V.I.S");
        title.setTextSize(30);
        title.setTextColor(Color.CYAN);
        title.setGravity(Gravity.CENTER);
        layout.addView(title);

        TextView subtitle = new TextView(this);
        subtitle.setText("YOUR PERSONAL AI ASSISTANT");
        subtitle.setTextColor(Color.LTGRAY);
        subtitle.setGravity(Gravity.CENTER);
        layout.addView(subtitle);

        apiKey = new EditText(this);
        apiKey.setHint("Enter Gemini API Key");
        apiKey.setSingleLine(true);
        apiKey.setTextColor(Color.WHITE);
        apiKey.setHintTextColor(Color.GRAY);
        apiKey.setInputType(129);
        apiKey.setText(prefs.getString("api_key", ""));
        layout.addView(apiKey);

        Button save = new Button(this);
        save.setText("SAVE API KEY");
        layout.addView(save);
        save.setOnClickListener(v -> {
            prefs.edit().putString("api_key", apiKey.getText().toString().trim()).apply();
            status.setText("API Key saved on this device.");
        });

        status = new TextView(this);
        status.setText("JARVIS ONLINE - Ready");
        status.setTextColor(Color.GREEN);
        status.setPadding(0, 15, 0, 15);
        layout.addView(status);

        messages = new LinearLayout(this);
        messages.setOrientation(LinearLayout.VERTICAL);
        layout.addView(messages);

        question = new EditText(this);
        question.setHint("Ask JARVIS anything...");
        question.setTextColor(Color.WHITE);
        question.setHintTextColor(Color.GRAY);
        layout.addView(question);

        Button send = new Button(this);
        send.setText("SEND TO JARVIS");
        layout.addView(send);
        send.setOnClickListener(v -> sendMessage());

        Button voice = new Button(this);
        voice.setText("🎤 SPEAK TO JARVIS");
        layout.addView(voice);
        voice.setOnClickListener(v -> startVoice());

        addMessage("JARVIS", "Hello Sir! Main taiyar hoon. Aap mujhse kuch bhi pooch sakte hain.");
    }

    void addMessage(String who, String message) {
        TextView item = new TextView(this);
        item.setText(who + ": " + message);
        item.setTextColor(Color.WHITE);
        item.setTextSize(16);
        item.setPadding(12, 12, 12, 12);
        messages.addView(item);
    }

    void sendMessage() {
        String prompt = question.getText().toString().trim();
        String key = apiKey.getText().toString().trim();

        if (prompt.isEmpty()) {
            status.setText("Please enter your question.");
            return;
        }

        if (key.isEmpty()) {
            status.setText("Please enter your Gemini API Key.");
            return;
        }

        prefs.edit().putString("api_key", key).apply();
        question.setText("");
        addMessage("YOU", prompt);
        status.setText("JARVIS is thinking...");

        new Thread(() -> {
            String answer = askGemini(key, prompt);
            runOnUiThread(() -> {
                addMessage("JARVIS", answer);
                status.setText("JARVIS ONLINE");
                if (tts != null) tts.speak(answer, TextToSpeech.QUEUE_FLUSH, null, "jarvis_reply");
            });
        }).start();
    }

    String askGemini(String key, String prompt) {
        HttpURLConnection connection = null;
        try {
            URL url = new URL(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + key
            );

            JSONObject part = new JSONObject();
            part.put("text", prompt);

            JSONArray parts = new JSONArray();
            parts.put(part);

            JSONObject content = new JSONObject();
            content.put("parts", parts);

            JSONArray contents = new JSONArray();
            contents.put(content);

            JSONObject body = new JSONObject();
            body.put("contents", contents);

            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setConnectTimeout(20000);
            connection.setReadTimeout(30000);
            connection.setDoOutput(true);
            connection.setRequestProperty("Content-Type", "application/json");

            try (OutputStream output = connection.getOutputStream()) {
                output.write(body.toString().getBytes("UTF-8"));
            }

            int code = connection.getResponseCode();
            InputStream stream = code >= 200 && code < 300
                ? connection.getInputStream() : connection.getErrorStream();

            BufferedReader reader = new BufferedReader(new InputStreamReader(stream));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();

            JSONObject result = new JSONObject(response.toString());

            if (code < 200 || code >= 300) {
                return "Gemini API Error: " + result.optJSONObject("error").optString("message", "Request failed");
            }

            return result.getJSONArray("candidates")
                .getJSONObject(0)
                .getJSONObject("content")
                .getJSONArray("parts")
                .getJSONObject(0)
                .optString("text", "No response received.");

        } catch (Exception e) {
            return "Connection Error: " + e.getMessage();
        } finally {
            if (connection != null) connection.disconnect();
        }
    }

    void startVoice() {
        try {
            Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN");
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to JARVIS");
            startActivityForResult(intent, 100);
        } catch (Exception e) {
            status.setText("Voice recognition is not available.");
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 100 && resultCode == RESULT_OK && data != null) {
            String spoken = data.getStringArrayListExtra(
                RecognizerIntent.EXTRA_RESULTS).get(0);
            question.setText(spoken);
            sendMessage();
        }
    }

    @Override
    protected void onDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        super.onDestroy();
    }
}
