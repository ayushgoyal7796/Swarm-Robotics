package com.example.saikiran.swarm_1;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;


public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);             //layout file to be viewed is activity_main

    }

    public void firstf(View view)
    {
        Intent intent = new Intent(this, first.class);      // Starting a new activity when pressed the first button in MainActivity
        startActivity(intent);                              // Calling the new activity
    }

    public void secondf(View view)
    {
        Intent intent = new Intent(this, second.class);    // Starting a new activity when pressed the second button in MainActivity
        startActivity(intent);                              // Calling the new activity
    }


}
