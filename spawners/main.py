from spawners.kuber import KubernetesSpawner

if __name__ == '__main__':
    spawner = KubernetesSpawner()
    spawner.spawn(image="serverhub-servers:serverhub-homework-master")
