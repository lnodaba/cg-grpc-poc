using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Grpc.Net.Client;
using GrpcAcronymsClient;

namespace grpc_client.services
{
    internal class TrainsetContentServiceService
    {
        private readonly TrainsetContentService.TrainsetContentServiceClient _client;

        public TrainsetContentServiceService()
        {
            var channel = GrpcChannel.ForAddress("http://localhost:50051");
            _client = new TrainsetContentService.TrainsetContentServiceClient(channel);
        }

        public async Task<TrainsetContent> create(TrainsetContent acronym)
        {
            return await _client.createAsync(acronym);
        }

        public async Task<TrainsetContentList> get_all()
        {
            return await _client.get_allAsync(new Empty());
        }

        public async Task<TrainsetContent> update(TrainsetContent acronym)
        {
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> delete(TrainsetContent acronym)
        {
            return await _client.deleteAsync(acronym);
        }
    }
}
