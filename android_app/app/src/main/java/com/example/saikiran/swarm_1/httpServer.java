package com.example.saikiran.swarm_1;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class httpServer
{
    public static String host_url="http://192.168.0.124:8080/getdata";    //IP_ADDRESS AND PORT NUMBER OF SERVER

    public static String send_server(JSONObject jsonObject) throws JSONException
    {
        HttpURLConnection con = null;
        OutputStream outputStream = null;
        StringBuffer response=null;

        try
        {
            con=(HttpURLConnection)(new URL(host_url)).openConnection();
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.connect();
            outputStream=new BufferedOutputStream(con.getOutputStream());
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, "UTF-8"));
            writer.write(jsonObject.toString());
            Log.i(jsonObject.toString(),"\n");

            writer.close();
            outputStream.close();

            int responseCode = con.getResponseCode();
            System.out.println("\nSending 'POST' request to URL : " + host_url);
            System.out.println("Response Code : " + responseCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            System.out.println("Response in universal: " + response.toString());
            return response.toString();

        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        return null;
    }
}
