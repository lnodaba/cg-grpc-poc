using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GrpcAcronymsClient;
using Xunit;

namespace grpc_client.tests;
public class TrainsetServiceTest
{
    private readonly services.TrainsetServiceService _service;

    public TrainsetServiceTest()
    {
        _service = new services.TrainsetServiceService();
    }


    [Fact]
    public async Task a_Create()
    {
        // Arrange
        var acronym = new Trainset
        {
            Description= "start descripton"
        };

        // Act
        var created = await _service.create(acronym);

        // Assert
        Assert.NotNull(created);
        Assert.NotNull(created.CreateDt);

        Assert.Equal(acronym.Description, created.Description);

    }

    [Fact]
    public async Task b_GetAll()
    {
        // Arrange

        // Act
        var result = await _service.get_all();

        // Assert
        Assert.NotNull(result.List);

    }

    [Fact]
    public async Task c_Update()
    {
        // Arrange
        var result = await _service.get_all();
        var last = result.List[result.List.Count - 1];
        

        // Act
        var updated = await _service.update(last);

        // Assert
        

    }

    [Fact]
    public async Task d_Delete()
    {

        // Arrange
        var result = await _service.get_all();
        var last = result.List[result.List.Count - 1];

        // Act
        await _service.delete(last);

        var res = await _service.get_all();

        foreach (var item in res.List)
        {
            Assert.NotEqual(last.Id, item.Id);
        }

    }
}
