package dist_mat_mr;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.eclipse.jetty.util.ArrayUtil;

public class final_reducer extends Reducer<IntWritable, Text, NullWritable, Text> {
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
            final List<String> line = new ArrayList<>(Arrays.asList(val.toString().split(",")));
            // format is output sender, destination and rtt with , as seperator
            String node = line.get(0);
            line.remove(0);
            // Add node name and line of matrix for that node to the hashmap
            nodeMap.put(node, line.toString().replace("[", "").replace("]", ""));
        }
        final StringBuilder output = new StringBuilder();
        output.append("---Start_Of_" + key.toString() + "---\n");
        for (int i = 0; i < destination_Orders.length; ++i) {
            output.append(nodeMap.get(destination_Orders[i]) + "\n");
        }
        output.append("---End_Of_" + key.toString() + "---\n");
        // context.write(key, new Text(nodeMap.toString()));
        context.write(NullWritable.get(), new Text(output.toString()));
    }
}
