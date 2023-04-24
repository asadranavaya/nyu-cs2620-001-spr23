package dist_mat_mr;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class MatrixMapper extends Mapper<LongWritable, Text, IntWritable, Text> {
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        // Line format is "lineNum, sender, destination, time_sent, rtt, time_sent+rtt"
        final String[] temp = value.toString().split(",");

        final Integer lineNum = Integer.parseInt(temp[0]);
        // output sender, destination and rtt with | as seperator
        final String outputRtt = temp[1] + "," + temp[2] + "," + temp[4];
        context.write(new IntWritable(lineNum), new Text(outputRtt));
    }
}
