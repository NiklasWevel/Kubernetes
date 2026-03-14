# The beginner mistake

```mermaid
flowchart TB

subgraph KubernetesCluster["Kubernetes Cluster"]

    AppA["App A"]
    AppB["App B"]

    subgraph CNPGCluster["CNPG Cluster"]
        DatabaseA[(Database A)]
        DatabaseB[(Database B)]
    end

end

subgraph S3["s3.wevelsiep.com"]
    Bucket[(S3 Bucket)]
end

AppA --> DatabaseA
AppB --> DatabaseB

CNPGCluster -- S3 Key --> S3

```

In the beginning, I thought it was a good idea to run every database in a single massive CNPG cluster.
I noticed my mistake when I tried to test my backups: CNPG can only restore databases at the cluster level.
If I make a mistake in Database A, I would need to restore the entire cluster, affecting even databases that aren't impacted.

I checked the resource usage of the CNPG cluster:

```bash
NAME                        CPU(cores)   MEMORY(bytes)   
database-postgres-cluster-1   11m          84Mi    
```
At that moment, I realized that a single cluster for all apps was not ideal.
Instead, having one cluster per app would be safer and not that resource heavy. CNPG is really lightweight in that regard. 


# The refactor

```mermaid

flowchart TB

subgraph KubernetesCluster["Kubernetes Cluster"]

    AppA["App A"]
    AppB["App B"]

    subgraph CNPGClusterA["CNPG Cluster A"]
        DatabaseA[(Database A)]
    end

    subgraph CNPGClusterB["CNPG Cluster B"]
        DatabaseB[(Database B)]
    end

end

subgraph S3["s3.wevelsiep.com"]
    S3BucketA[(S3 Bucket A)]
    S3BucketB[(S3 Bucket B)]
end

AppA --> CNPGClusterA
AppB --> CNPGClusterB

DatabaseA -- S3 Key A --> S3BucketA
DatabaseB -- S3 Key B --> S3BucketB

```

During the refactor, I split the single S3 bucket into multiple buckets.

Now, each app gets its own CNPG cluster, S3 bucket, and backup key, making it possible to restore individual databases.  
Additionally, this provides separation between databases both at the cluster level and at the S3 bucket level, improving isolation and safety.

# Conclusion

I realized this issue during a backup test. In production, everything worked as expected.  

This experience once again shows me the importance of using and testing my setup.
If I hadn't caught this beforehand, I would have discovered it at a very bad time: when I *must* restore a backup, not when I *want* to.