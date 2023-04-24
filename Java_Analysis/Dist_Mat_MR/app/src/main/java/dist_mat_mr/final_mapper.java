package dist_mat_mr;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class final_mapper extends Mapper<LongWritable, Text, IntWritable, Text> {
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        // Line format is "lineNum, sender, destination, time_sent, rtt, time_sent+rtt"
        final String[] temp = value.toString().split(",");

        final Integer lineNum = Integer.parseInt(temp[0]);
        // output sender, destination and rtt with | as seperator
        // Have to copy array, time of O(n) :/
        final StringBuilder output = new StringBuilder();
        for (int i = 1; i < temp.length; ++i) {
            if (i + 1 >= temp.length) {
                output.append(temp[i]);
            } else {
                output.append(temp[i] + ",");
            }
        }
        context.write(new IntWritable(lineNum), new Text(output.toString()));
    }
}
