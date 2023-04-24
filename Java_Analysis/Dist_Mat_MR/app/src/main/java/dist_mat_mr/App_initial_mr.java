/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package dist_mat_mr;

import java.io.File;
import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class App_initial_mr {
    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        final String[] folder_prefixes = { "aws_frankfurt", "aws_nor_cal", "aws_ohio", "aws_oregon", "aws_sao_paulo",
                "aws_stockholm", "azure_brazil", "azure_france", "azure_japan_east", "azure_south_africa_north",
                "azure_us_east", "gcp_asia_east", "gcp_australia_southeast", "gcp_europe_north", "gcp_us_central",
                "gcp_us_south" };

        // final Configuration conf = new Configuration();
        // final Job job = Job.getInstance(conf, "Initial Node join and map to first
        // part of distance matrix data");
        for (int i = 0; i < folder_prefixes.length; ++i) {
            Job job = Job.getInstance();
            job.setJarByClass(App_initial_mr.class);
            job.setJobName("Initial Node join and map to first part of distance matrix / data");
            final Path inputPath = new Path(args[0] + "/" + folder_prefixes[i]);
            FileInputFormat.addInputPath(job, inputPath);
            final File file = new File(inputPath.toString() + "_MappedOutput");
            FileOutputFormat.setOutputPath(job, new Path(file.getPath()));
            job.setMapperClass(MatrixMapper.class);
            job.setMapOutputKeyClass(IntWritable.class);
            job.setReducerClass(MatrixReducer.class);
            job.setNumReduceTasks(1);
            job.waitForCompletion(true);
        }

    }
}