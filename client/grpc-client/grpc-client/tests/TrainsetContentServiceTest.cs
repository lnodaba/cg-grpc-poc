using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GrpcAcronymsClient;
using Xunit;

namespace grpc_client.tests;

public class TrainsetContentServiceTest
{
    private readonly services.TrainsetContentServiceService _service;

    public TrainsetContentServiceTest()
    {
        _service = new services.TrainsetContentServiceService();
    }

    [Fact]
    public async Task a_Create()
    {
        // Arrange
        var dto = new TrainsetContent
        {
            Role = "user"
        };

        // Act
        var created = await _service.create(dto);

        // Assert
        Assert.NotNull(created);
        Assert.Equal("user", created.Role);
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
        last.TraindataId = 2;

        // Act
        var updated = await _service.update(last);

        // Assert
        Assert.Equal(last.TraindataId, updated.TraindataId);

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
