package dist_mat_mr;

import java.io.IOException;
import java.util.HashMap;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class MatrixReducer extends Reducer<IntWritable, Text, NullWritable, Text> {
    public final String[] destination_Orders = { "20.120.81.61", "20.216.155.104", "20.89.94.125", "4.228.99.39",
            "20.164.218.209", "34.69.69.92", "34.88.245.139", "15.228.18.192", "130.211.244.244", "18.191.228.87",
            "34.87.241.234", "34.174.200.217", "54.219.89.236", "35.89.17.138", "18.185.105.74", "16.16.123.217" };
    // Save memory and declare above
    static final HashMap<String, String> nodeMap = new HashMap<>();

    // @Override
    // public void setup(Context context) throws IOException{
    // //Setup the reduce to know the order of destinations for IP
    //
    // }
    @Override
    public void reduce(IntWritable key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        // Add to hashmap
        // Then iterate over array order and grab from hashmap the output order
        nodeMap.clear();
        int j = 0;
        String sendingNode = "";
        for (final Text val : values) {
            final String[] line = val.toString().split(",");
            // format is output sender, destination and rtt with , as seperator
            if (j == 0) {
                // put the sending node in the map only once
                nodeMap.put(line[0], "0");
                sendingNode = line[0];
                ++j;
            }
            nodeMap.put(line[1], line[2]);
        }
        final StringBuilder output = new StringBuilder();
        output.append(key.toString() + "," + sendingNode + ",");
        for (int i = 0; i < destination_Orders.length; ++i) {
            if (i + 1 >= destination_Orders.length) {
                output.append(nodeMap.get(destination_Orders[i]));
            } else {
                output.append(nodeMap.get(destination_Orders[i]) + ",");
            }
        }
        // context.write(key, new Text(nodeMap.toString()));
        context.write(NullWritable.get(), new Text(output.toString()));
    }
}
