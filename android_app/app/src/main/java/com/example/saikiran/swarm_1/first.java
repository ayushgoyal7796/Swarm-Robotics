package com.example.saikiran.swarm_1;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import org.json.JSONException;
import org.json.JSONObject;


public class first extends MainActivity {
    public int k=0;

    JSONObject jsonObject=null;   //initializing JSONObject for data transfer
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_first);

    }

    public void square(View view) {                                //called when square button is pressed
        try {
            jsonObject=new JSONObject();
            jsonObject.put("command", 1);                          //load the input data into jsonObject
            new SendPi(getApplicationContext()).execute();         //call the data transfer function
        }
        catch(JSONException e){
            e.printStackTrace();
        }

    }

    ///////////////////////Similar procedure is followed for all the remaining buttons///////////////////////////

    public void rectangle(View view) {
        try {
            jsonObject=new JSONObject();
            jsonObject.put("command", 2);
            new SendPi(getApplicationContext()).execute();
        }
        catch(JSONException e){
            e.printStackTrace();
        }
    }

    public void line(View view) {
        try {
            jsonObject=new JSONObject();
            jsonObject.put("command", 3);
            new SendPi(getApplicationContext()).execute();
        }
        catch(JSONException e){
            e.printStackTrace();
        }
    }

    public void switch1(View view) {
        try {
            jsonObject=new JSONObject();
            jsonObject.put("command", 4);
            new SendPi(getApplicationContext()).execute();
        }
        catch(JSONException e){
            e.printStackTrace();
        }
    }

    public void rotate(View view) {
        try {
            jsonObject=new JSONObject();
            jsonObject.put("command", 5);
            new SendPi(getApplicationContext()).execute();
        }
        catch(JSONException e){
            e.printStackTrace();
        }
    }
    public void reset(View view) {
        try {
            jsonObject=new JSONObject();
            jsonObject.put("command", 0);
            new SendPi(getApplicationContext()).execute();
        }
        catch(JSONException e){
            e.printStackTrace();
        }
    }

    private class SendPi extends AsyncTask<Void,Void,Void> {     //data transfer class definition
        Context context;

        public SendPi(Context c) {
            context = c;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected Void doInBackground(Void... params) {
            try {
                httpServer sender = new httpServer();
                sender.send_server(jsonObject);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(Void v)
        {
            super.onPostExecute(v);
        }
    }

}
