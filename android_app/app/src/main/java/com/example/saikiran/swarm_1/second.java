package com.example.saikiran.swarm_1;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;


public class second extends AppCompatActivity {

    private RelativeLayout activity_second = null;
    private double x[]={0.0,0.0,0.0,0.0};
    private double y[]={0.0,0.0,0.0,0.0};
    public int j=0;
    JSONObject jsonObject2=null;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        activity_second = (RelativeLayout) findViewById(R.id.activity_second);


        activity_second.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                TextView t=(TextView)findViewById(R.id.textView);
                x[j] = event.getX();
                y[j] = event.getY();
                t.setText("Waiting");

                if (event.getAction() == MotionEvent.ACTION_DOWN) {


                    if(j==3){
                        try{
                        JSONArray arrayx = new JSONArray();
                        JSONArray arrayy = new JSONArray();
                        for (int a = 0; a <4 ; a++) {
                            arrayx.put(x[a]);
                            arrayy.put(y[a]);

                        }

                        jsonObject2 =new JSONObject();
                        jsonObject2.put("xdata1",arrayx);
                        jsonObject2.put("ydata1",arrayy);
                            new SendPi(getApplicationContext()).execute();

                        }catch(JSONException e){
                            e.printStackTrace();
                        }
                    t.setText("Sent");
                    }

                    j++;
                    if(j>3) j=0;

                }
                return true;
            }
        });

    }



    private class SendPi extends AsyncTask<Void,Void,Void> {
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
                sender.send_server(jsonObject2);
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
